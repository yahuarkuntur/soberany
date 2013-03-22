import pygame
from pygame.locals import *

import event
from event import *

import widget
from widget import *

import utils
from utils import *

import os

## images[0] = normal
## images[1] = pressed


class Button(Widget):
    def __init__(self, name, images, pos, container=None):
        Widget.__init__(self, container)
        self.images = images
        self.name = name
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft  = pos
        self.clickEvent = False
        self.clicked = False
        self.font = pygame.font.Font(os.path.join('fonts','vera.ttf'),14)
        self.text = self.font.render(name,1,WHITE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center


    def move(self, pos):
        self.rect.center  = pos

    def update(self,screen):
        if self.focused and not self.clickEvent:
            #pygame.time.wait(50)
            self.text = self.font.render(self.name,1,GRAY)
            self.image = self.images[0]
##        if not self.focused and self.clickEvent:
##            #pygame.time.wait(50)
##            self.text = self.font.render(self.name,1,GRAY)
##            self.image = self.images[0]
##            self.clickEvent=False
        elif self.clickEvent:
            # button clicked
            self.text = self.font.render(self.name,1,GRAY)
            self.image = self.images[1]
            self.draw(screen)
            #pygame.time.wait(50)
            self.clickEvent=False
        elif not self.clickEvent:
            self.image = self.images[0]
            self.text = self.font.render(self.name,1,WHITE)
        elif not self.focused:
            self.clickEvent=False
            self.image = self.images[0]
            self.text = self.font.render(self.name,1,WHITE)
            
        self.draw(screen)

    def click(self):
        #self.cambios = True
        self.clickEvent = True
        self.clicked = True

    def isClicked(self):
        return self.clicked 

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text,self.text_rect)
        
        
    def notify(self, event):
        key = event.keyState()
        mouse_button = event.mouseState()            
        mouse_pos = event.mousePos()
##        if key[K_DOWN] and self.focused and not self.clickEvent:
##            event.name = "Key pressed"
##            print 'key pressed'
##            self.click()
        if mouse_button[0] and not self.rect.collidepoint(mouse_pos):
            self.clickEvent = False
            self.focused = False
            self.clicked = False
        elif mouse_button[0] and self.focused and not self.clickEvent:
            #event.nombre = "Left mouse click"
            self.click()
        elif self.rect.collidepoint(mouse_pos) and not self.clickEvent:
            #event.nombre = "Mouse over"
            self.focused = True
            self.clicked = False
        elif not self.clickEvent:
            self.focused = False
            self.clicked = False



#===================================================================================
#                               FUNCION PRINCIPAL
#===================================================================================
##def main():
##    pygame.init()
##    screen = pygame.display.set_mode((200,200),16)
##    back = pygame.Surface(screen.get_size(),16)
##
##    back.fill(WHITE)
##    screen.blit(back,(0,0))
##
##    clock = pygame.time.Clock()
##    
##    MyEvent = Event()
##
##
##    images = []
##    images.append(load_image(os.path.join('data'),'button.png'))
##    images.append(load_image(os.path.join('data'),'button_pressed.png'))
##    #images.append(load_image(os.path.join('data'),'button_pressed.png'))
##
##    button = Button('Click me',images,(100,50))
##    button2 = Button('Close me',images,(100,100))
##
##
##    while 1:
##        
##        clock.tick(40)
##        
##        for event in pygame.event.get():
##            if event.type == KEYDOWN:
##                if event.key == K_ESCAPE:
##                    return
##                
##        button.notify(MyEvent)
##        button2.notify(MyEvent)
##
##        if button.isClicked():
##            pass
##        if button2.isClicked():
##            return 
##
##        button.update(screen)
##        button2.update(screen)
##
##        pygame.display.flip()
##
##
##
##if __name__ == '__main__':
##    main()
    
