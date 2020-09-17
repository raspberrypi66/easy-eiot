#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys, pygame
from pygame.locals import *
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ['SDL_AUDIODRIVER'] = "dsp"
os.environ["SDL_FBDEV"] = "/dev/fb0"

size = width, height = 240,240

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill((255,128,0))
pygame.mouse.set_visible(False)
pygame.display.toggle_fullscreen()
font = pygame.font.Font("/home/pi/board_examples/fonts/Anakotmai-Medium.ttf", 17)
clock = pygame.time.Clock()

while(1):
    text = font.render("Hello World", True, (255,255,255))
    screen.blit(text, [0, 0])
    pygame.display.flip()
