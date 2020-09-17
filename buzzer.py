#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO 
import time 

class Buzzer(object):
    def __init__(self,pin=13):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
        self.p = GPIO.PWM(pin, 100)

    def beep(self,duration):
        self.p.start(1)
        self.p.ChangeFrequency(1200) 
        time.sleep(duration)
        self.p.stop()

    def playNote(self,freq,duration):
        self.p.start(1)
        self.p.ChangeFrequency(freq)
        time.sleep(duration)
        self.p.stop()
            

def main():
    buz=Buzzer(13)
    buz.beep(0.15)
    time.sleep(1)
    notes=[261,294,329,349,392,440,493,523.25]
    for note in notes:
        buz.playNote(note,0.1)

if __name__ == "__main__":
    main()
