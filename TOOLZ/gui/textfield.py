import pygame
from pygame.locals import *

import event
from event import *

import widget
from widget import *

import utils
from utils import *

import os


class TextField(Widget):
    def __init__(self, name, width, pos, maxchars = 10, container = None):
        Widget.__init__( self, container)
        self.name = name
        self.bgcolor = WHITE
        self.fcolor = BLACK
        self.resize(width)
        self.rect.topleft = pos
        self.text = ''
        self.textPos = (2, 2)
        ##self.limits(width, maxchars)
        self.maxchars = maxchars

    def resize(self, width):
        self.font = pygame.font.Font(os.path.join('data','vera.ttf'), 14)
        lineSize = self.font.get_linesize()
        self.rect = pygame.Rect((0, 0, width, lineSize + 5))
        image = pygame.Surface(self.rect.size).convert()
        image.fill(self.bgcolor)
        self.image = image
        pygame.draw.rect(image, BLACK, self.rect, 1)
        self.clearImage = image.convert()

##    def limits(self, ancho, maxcars):
##        pass
##        LoMaximoInCars = int( ancho / (TAMTEXT/2.5) )
##        if maxcars == 0:
##            self.maxInRect = LoMaximoInCars # Los caracteres q alcanzan
##        else:
##            if maxcars <= LoMaximoInCars:
##                self.maxInRect = maxcars # Los caracteres q se desean alcanzar
##            else: # Se respeta igual que alcancen en la caja para no hacer scrolling
##                self.maxInRect = LoMaximoInCars

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self,screen):
        if not self.changed:
            return
        text = self.text
        if self.focused:
            text += '|'
        textSurf = self.font.render(text, 1, self.fcolor)
        self.image.blit(self.clearImage, (0,0))
        self.image.blit(textSurf, self.textPos)
        self.draw(screen)

    def click(self):
        self.focused = True
        self.changed = True

    def setText(self, text):
        self.text = text
        self.focused = True
        self.changed = True

    def getText(self):
        return self.text

    def notify(self, event, key):
        keyb = event.keyState()
        mouse_button = event.mouseState()            
        mouse_pos = event.mousePos()
        # handle keys
        if key > 256:
            return
##        if self.focused and keyb[K_LEFT] and key != 0:
##            return
##        elif self.focused and keyb[K_RIGHT] and key != 0:
##            return
        if self.focused and keyb[K_BACKSPACE] and key != 0:
            newText = self.text[:( len(self.text) - 1 )]
            self.setText(newText)
        elif self.focused and key != 0 and not keyb[K_BACKSPACE]:
            if len(self.text) < self.maxchars: 
                newText = self.text + chr(key) 
                self.setText(newText)
        elif mouse_button[0] and self.rect.collidepoint(mouse_pos):
            self.click()                        
        elif mouse_button[0] and not self.rect.collidepoint(mouse_pos) and self.focused:
            self.setFocus(False)


#===================================================================================
#                               FUNCION PRINCIPAL
#===================================================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((200,200),16)
    back = pygame.Surface(screen.get_size(),16)
    color = (255,255,255)
    back.fill(color)
    screen.blit(back,(0,0))

    clock = pygame.time.Clock()
    
    MyEvent = Event()

    textbox = Input('',100,(100,50))

    

    while 1:
        clock.tick(40)

        key = 0

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                else:
                    key = event.key

        textbox.notify(MyEvent, key)

        textbox.update(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
    
