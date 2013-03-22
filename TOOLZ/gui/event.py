import pygame
from pygame.locals import *

class Event:
    def __init__(self):
        self.name = "Generic Event"
        self.keyState = pygame.key.get_pressed
        self.mouseState   = pygame.mouse.get_pressed
        self.mousePos   = pygame.mouse.get_pos
            
