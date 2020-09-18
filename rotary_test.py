from RPi import GPIO
from time import sleep

dt_pin = 5
clk_pin = 6
sw_pin = 16
counter = 128
clkLastState = 0

def rotary_callback(channel):
    global clkLastState
    global counter
    clkState = GPIO.input(clk_pin)
    if clkState != clkLastState:
        dtState = GPIO.input(dt_pin)
        if dtState != clkState:
            counter = [lambda:counter+1, lambda:0][counter>254]() 
        else:
            counter =  [lambda:counter-1, lambda:255][counter<1]()
    clkLastState = clkState
    print("Counter : "+str(counter)+" Press to reset")

def sw_callback(channel):
    global counter
    counter = 128
    print("Reset counter to 128")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk_pin, GPIO.IN)
GPIO.setup(dt_pin, GPIO.IN)
GPIO.setup(sw_pin, GPIO.IN)

GPIO.add_event_detect(clk_pin, GPIO.FALLING  , callback=rotary_callback , bouncetime=10)
GPIO.add_event_detect(sw_pin, GPIO.FALLING , callback=sw_callback, bouncetime=300)

while(1):
    sleep(0.1)

