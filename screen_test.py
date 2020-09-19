#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, pygame
from pygame.locals import *
import os
import random

#Config for tiny screen
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ['SDL_AUDIODRIVER'] = "dsp"
os.environ["SDL_FBDEV"] = "/dev/fb0"
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 240,240
BALL_SIZE=10

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.mouse.set_visible(False)#hide mouse pointer
pygame.display.toggle_fullscreen()#show full screen

screen.fill((255,255,255))#fill screen color

font = pygame.font.Font("/home/pi/board_examples/fonts/Anakotmai-Medium.ttf", 17)
clock = pygame.time.Clock()

ballX=random.randrange(2, 100)
ballY=100
ballChangeX=3
ballChangeY=-2

while(1):
    #draw 3 color background
    pygame.draw.rect(screen,(0,0,255),(0,0,80,240))
    pygame.draw.rect(screen,(255,255,255),(80,0,80,240))
    pygame.draw.rect(screen,(255,0,0),(160,0,80,240))
    
    #moveBall()
    ballX += ballChangeX
    ballY += ballChangeY

    # Bounce the ball if needed
    if ballY > ((SCREEN_HEIGHT-100)- BALL_SIZE) or ballY < BALL_SIZE:
        ballChangeY *= -1
    if ballX > (SCREEN_WIDTH - BALL_SIZE) or ballX < BALL_SIZE:
        ballChangeX*= -1

    pygame.draw.circle(screen,(5,255,5),(ballX,ballY),BALL_SIZE)#Draw ball

    #Draw black background
    pygame.draw.rect(screen,(5,5,5),(10,140,220,90))
    #Draw text
    text = font.render("Hello World", True, (0,255,255))
    screen.blit(text, [70, 150])
    text = font.render("สวัสดีชาวโลก", True, (255,0,255))
    screen.blit(text,[70,180]) 

    clock.tick(60)# Limit to 60 frames per second
    pygame.display.flip()#show on screen
