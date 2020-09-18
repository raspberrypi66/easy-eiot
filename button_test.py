#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from RPi import GPIO
from time import sleep

press_sw_pin = 26
press_sw_counter = 0

def press_sw_callback(channel):
    global press_sw_counter
    press_sw_counter += 1
    print("Button switch press "+str(press_sw_counter)+" times")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(press_sw_pin, GPIO.IN)
GPIO.add_event_detect(press_sw_pin, GPIO.FALLING , callback=press_sw_callback, bouncetime=300)

print("Press button switch to increase counter")
while(1):
    sleep(0.1)




