#!/usr/bin/python

import sys
import getopt
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import re
import json
import time

PERSONALITY_FILE_PATH = "./emotion_mappings/responsive.json"

os.system("sudo killall -9 pocketsphinx_continuous 2> /dev/null")
proc = subprocess.Popen(["sudo pocketsphinx_continuous -adcdev plughw:1,0 -dict ./bot.dic  2> /dev/null"], stdout=subprocess.PIPE, shell=True, bufsize=1)


def load_personality():
	with open(PERSONALITY_FILE_PATH, 'r') as inputFile:
		personality = json.load(inputFile)
		print("Personality is loaded. Description: [%s]" % (personality["desc"]))
		return personality
personality = load_personality()


import api

def default_action():
        api.PlayAction(66)
	
def take_action(text, personality):
	emotion = None
	degree = None
	api_map = {'happy3': 4, 'happy2': 5, 'anger2': 6, 'anger3': 7, 'fear3': 11,
			   'fear2': 12, 'surprise2': 13, 'surprise3': 14, 'sad2': 17, 'sad3': 18}
	
	for word in text.split(' '):
		if emotion is None:
			emotion = personality["keywords"].get(word, None)
		if degree is None:
			degree = personality["degree"].get(word, None)
			
	if emotion is None:
		emotion = personality["keywords"]["_default"]
	if degree is None:
		degree = personality["degree"]["_default"]

	print("Got emotion [%s] with degree [%d]." % (emotion, degree))
	rme_page = api_map.get(emotion + str(degree), None)
	if rme_page:
		api.PlayAction(rme_page)
	else:
		print("Could not understand, playing default reaction.")
		default_action()


def init_rme_api():
	if api.Initialize():
		print("Initialized Node Server")
		#play_page_for_sit()
	else:
		print("Initialization failed")
		sys.exit(1)

		
init_rme_api()
default_action()

last_action_time = time.time()
try:
	while True:
		for line in iter(proc.stdout.readline, b''):
			row = line[:-1]
			match = re.match(r"(\d+)\:(.*)", row)
			if match and time.time() - last_action_time > 8.0:
				seq =  match.groups()[0]
				text = match.groups()[1]
				print "\nGet text:", text
				take_action(text, personality)
				last_action_time = time.time()
			else:
				print row
			
except KeyboardInterrupt:
	print "Exiting..."
	api.ServoShutdown()

