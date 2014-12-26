#!/usr/bin/python

import RPi.GPIO as GPIO 
import time
import sys

from threading import Thread

button = 7

r = 18
b = 23
g = 24 
y = 25 
pins = [r, b, g, y]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in [r, b, g, y]:
	GPIO.setup(pin, GPIO.OUT)

GPIO.setup(button, GPIO.IN)


dah = .5
dit = .1
char2morse = {' ':[dit, dit, dit], 
			  'a':[dit, dah], 
			  'b':[dah, dit, dit, dit],
			  'c':[dah, dit, dah, dit],
			  'd':[dah, dit, dit],
			  'e':[dit],
			  'f':[dit, dit, dah, dit],
			  'g':[dah, dah, dit],
			  'h':[dit, dit, dit, dit],
			  'i':[dit, dit],
			  'j':[dit, dah, dah, dah],
			  'k':[dah, dit, dah],
			  'l':[dit, dah, dit, dit],
			  'm':[dah, dah],
			  'n':[dah, dit],
			  'o':[dah, dah, dah],
			  'p':[dit, dah, dah, dit],
			  'q':[dah, dah, dit, dah],
			  'r':[dit, dah, dit],
			  's':[dit, dit, dit],
			  't':[dah],
			  'u':[dit, dit, dah],
			  'v':[dit, dit, dit, dah],
			  'w':[dit, dah, dah],
			  'x':[dah, dit, dit, dah],
			  'y':[dah, dit, dah, dah],
			  'z':[dah, dah, dit, dit],
			  '0':[dah, dah, dah, dah, dah],
			  '1':[dit, dah, dah, dah, dah],
			  '2':[dit, dit, dah, dah, dah],
			  '3':[dit, dit, dit, dah, dah],
			  '4':[dit, dit, dit, dit, dah],
			  '5':[dit, dit, dit, dit, dit],
			  '6':[dah, dit, dit, dit, dit],
			  '7':[dah, dah, dit, dit, dit],
			  '8':[dah, dah, dah, dit, dit],
			  '9':[dah, dah, dah, dah, dit]}

class MorsePlayer(Thread):
	def __init__ (self, message):
		Thread.__init__(self)
		self.message = message
		self.interrupted = False

	def interrupt(self):
		self.interrupted = True

	def run(self):
		for c in message:
			if self.interrupted:
				break
			print c, char2morse[c.lower()]
			if c == ' ':
				blink(y, dah, dit)
				continue
			for m in char2morse[c.lower()]:
				blink(r, m, dah)
			blink(g, dah, dah)
		
		for pin in pins:
			GPIO.output(pin, False)


def blink(pin, onTime, offTime):
	GPIO.output(pin, True)
	time.sleep(onTime)
	GPIO.output(pin, False)
	time.sleep(offTime)

def rainbow():
	for pin in pins:
		blink(pin, dit, 0)
				

if __name__ == '__main__':
	
	if len(sys.argv) > 1:
		message = sys.argv[1]
	else:
		message = 'hi clara'

	try:
		showRainbowPeriod = 3
		lastPress = time.time() - 1	
		lastRainbow = time.time() - showRainbowPeriod
		player = None
		while True:	
			if GPIO.input(button) == True and time.time() - lastPress > 1:
				lastPress = time.time()
				if player is not None and player.isAlive():
					player.interrupt()
					player.join()

				player = MorsePlayer(message)
				player.start()			
			elif time.time() - lastRainbow >= showRainbowPeriod and (player is None or not player.isAlive()):
				lastRainbow = time.time()
				rainbow()

	except:
			print 'bye'
			if player is not None and player.isAlive():
				player.interrupt()
				player.join()

			GPIO.cleanup()
