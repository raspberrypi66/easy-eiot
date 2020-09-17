#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
credit http://codelectron.com/rotary-encoder-with-raspberry-pi/
'''
import sys, pygame
from pygame.locals import *
import os
import smbus2 as smbus
import hs300x

from RPi import GPIO
from time import sleep,time
from neopixel import *
import buzzer

clk_pin = 6 
dt_pin = 5 
sw_pin = 16
press_sw_pin = 26
counter = 128

red_pin = 22
green_pin = 17
yellow_pin = 27

def rotary_callback(channel):  
    global clkLastState
    global counter
    try:
                clkState = GPIO.input(clk_pin)
                if clkState != clkLastState:
                        dtState = GPIO.input(dt_pin)
                        if dtState != clkState:
                                if counter<248:
                                    counter += 8
                                else :
                                    counter=0
                        else:
                                if counter>8:
                                    counter -= 8
                                else : 
                                    counter = 255
                        print("Encoder val :",counter)
                        screen.fill(RGBWheel(counter))
                        strip.setPixelColor(0, wheel((counter) & 255))
                        strip.show()
                        buz.playNote(60,0.02)
                clkLastState = clkState
    finally:
                pass

def sw_callback(channel):  
    buz.beep(0.1)
    print("press")

def press_sw_callback(channel):
    notes=[261,294,329,349,392,440,493,523.25]
    for note in notes:
        buz.playNote(note,0.1)
    print("sw press")



def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def RGBWheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        #return (pos * 3, 255 - pos * 3, 0)
        return ( 255 - pos * 3,pos * 3, 0)
    elif pos < 170:
        pos -= 85
        #return (255 - pos * 3, 0, pos * 3)
        return (0,255 - pos * 3,  pos * 3)
    else:
        pos -= 170
        #return (0, pos * 3, 255 - pos * 3)
        return ( pos * 3, 0 , 255 - pos * 3)

def getRGBfrom24Bit(RGBint):
    green =  RGBint & 255
    red = (RGBint >> 8) & 255
    blue =   (RGBint >> 16) & 255
    return  green,red,blue


if __name__ == '__main__':
    led_counter = 0

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clk_pin, GPIO.IN)
    GPIO.setup(dt_pin, GPIO.IN)
    GPIO.setup(sw_pin, GPIO.IN)
    GPIO.setup(press_sw_pin, GPIO.IN)

    GPIO.setup(red_pin, GPIO.OUT)
    GPIO.setup(green_pin, GPIO.OUT)  
    GPIO.setup(yellow_pin, GPIO.OUT)  

    # LED strip configuration:
    LED_COUNT      = 1      # Number of LED pixels.
    LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    buz=buzzer.Buzzer()
    clkLastState = GPIO.input(clk_pin)

    GPIO.add_event_detect(clk_pin, GPIO.FALLING  , callback=rotary_callback , bouncetime=5) 
    GPIO.add_event_detect(sw_pin, GPIO.FALLING , callback=sw_callback, bouncetime=300)  
    GPIO.add_event_detect(press_sw_pin, GPIO.FALLING , callback=press_sw_callback, bouncetime=1000)
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    strip.setPixelColor(0, wheel(counter))
    strip.show()
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ['SDL_AUDIODRIVER'] = "dsp"
    os.environ["SDL_FBDEV"] = "/dev/fb1"

    size = width, height = 240,240

    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill(RGBWheel(counter))
    pygame.mouse.set_visible(False)
    pygame.display.toggle_fullscreen()
    font = pygame.font.Font("/home/pi/board_examples/fonts/Anakotmai-Medium.ttf", 23)
    clock = pygame.time.Clock()
    start_blink = start = time()
    bus=smbus.SMBus(1)

    hsSensor = hs300x.Hs300x(bus)
    if(hsSensor.isAvailable()):
        hsSensor.MeasurementReq()
        temp = hsSensor.getTemperature()    
        humid = hsSensor.getHumidity()
    else:
        temp = 0.000
        humid = 0.000 
    
    while(1):
        if time() - start_blink >  0.5 :
            start_blink = time()
            if led_counter == 0 :
                GPIO.output(red_pin, GPIO.LOW)
            else : 
                GPIO.output(red_pin, GPIO.HIGH)

            if led_counter == 1 :
                GPIO.output(yellow_pin, GPIO.LOW)
            else :
                GPIO.output(yellow_pin, GPIO.HIGH)

            if led_counter == 2 :
                GPIO.output(green_pin, GPIO.LOW)
            else :
                GPIO.output(green_pin, GPIO.HIGH)

            if led_counter<2 :
                led_counter+=1 
            else :
                led_counter=0

        #read from sensor hs300x
        if time() - start > 5 :
            if(hsSensor.isAvailable()):
                print("start measurement")
                hsSensor.MeasurementReq()
                temp=hsSensor.getTemperature()
                humid=hsSensor.getHumidity()
                print(f'Temperature : {temp:.2f} C, Humidity : {humid:.2f} %')
                screen.fill(RGBWheel(counter))
            start = time()


        text = font.render("Color wheel : "+str(counter), True, (255,255,255))
        screen.blit(text, [15, 40])
        pygame.draw.rect(screen, (255,255,255), [1,110,238,100],3)
        text = font.render("Humidity : "+str(humid)[0:5], True, (255,255,255))
        screen.blit(text, [5, 120])
        text = font.render("Temperature : "+str(temp)[0:5], True, (255,255,255))
        screen.blit(text, [5, 160])   

        pygame.display.flip()

    GPIO.cleanup()
