#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 1      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

print("Change RGB color")
try:
    while(1):
        colorWipe(strip, Color(255, 0, 0),1000)  # Red wipe
        colorWipe(strip, Color(0, 255, 0),1000)  # Blue wipe
        colorWipe(strip, Color(0, 0, 255),1000)  # Green wipe
except KeyboardInterrupt:
    colorWipe(strip, Color(0,0,0), 10)   
    
