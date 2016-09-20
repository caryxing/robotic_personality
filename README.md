# Robotic Personality
Different robots will have different reactions to natural human laguage.

# Prerequisits
Install pocketsphinx.
```
sudo apt-get install pocketsphinx
``` 
refer: http://cmusphinx.sourceforge.net/wiki/raspberrypi

# Usage
1. Copy the motion_4096.bin file to ~/HROS1-Framework/Data/, this is the RME page configurations
2. Modify the path to the personality JSON file in voice_to_action.py
3. run "sudo python voice_to_action.py"
