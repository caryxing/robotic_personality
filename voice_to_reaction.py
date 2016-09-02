#!/usr/bin/python

import sys
import getopt
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import re
#import api
import json

PERSONALITY_FILE_PATH = "./emotion_mappings/easier_pleased.json"

os.system("sudo killall -9 pocketsphinx_continuous 2> /dev/null")
proc = subprocess.Popen(["sudo pocketsphinx_continuous -adcdev plughw:1,0 2> /dev/null"], stdout=subprocess.PIPE, shell=True, bufsize=1)

def take_action(text, personality):
	emotion = None
	degree = None
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


def load_personality():
	with open(PERSONALITY_FILE_PATH, 'r') as inputFile:
		personality = json.load(inputFile)
		print("Personality is loaded. Description: [%s]" % (personality["desc"]))
		#return {"keywords": personality["keywords"], "degree": personality["degree"]}
		return personality

personality = load_personality()

def init_rme_api():
	if api.Initialize():
		print("Initialized Node Server")
		play_page_for_sit()
	else:
		print("Initialization failed")
		sys.exit(1)

#init_rme_api()
		
try:
	while True:
		for line in iter(proc.stdout.readline, b''):
			row = line[:-1]
			match = re.match(r"(\d+)\: (.+)", row)
			if match:
				seq =  match.groups()[0]
				text = match.groups()[1]
				print "\nGet text:", text
				take_action(text, personality)
			else:
				print row
			
except KeyboardInterrupt:
	print "Exiting..."
	#api.ServoShutdown()

