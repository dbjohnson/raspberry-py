#!/usr/bin/python

import RPi.GPIO as GPIO
import time


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


if __name__ == '__main__':
    try:
        idx = len(pins) - 1
        while True:
            if GPIO.input(button):
                GPIO.output(pins[idx % len(pins)], False)
                idx += 1
                GPIO.output(pins[idx % len(pins)], True)
                time.sleep(0.2)
            else:
                GPIO.output(pins[idx % len(pins)], False)
    except:
        print 'bye'
        GPIO.cleanup()
