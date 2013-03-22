import pygame
from pygame.locals import *

class Widget(pygame.sprite.Sprite):
    def __init__(self, container=None):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.focused = False
        self.changed = True

    def setFocus(self, focus):
        self.focused = focus
        self.changed = True

    def destroy(self):
        self.container = None
        del self.container
        pygame.sprite.Sprite.kill(self)

