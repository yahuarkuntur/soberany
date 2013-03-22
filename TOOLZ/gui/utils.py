import pygame
from pygame.locals import *

import os

BLACK = (0,0,0)

#GRAY = (100,100,100)
GRAY = (150,150,150)

WHITE = (255,255,255)



def load_image(dir, name, colorkey=None):
    fullname = os.path.join(dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image
