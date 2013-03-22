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
## images[1] = selected

class CheckBox(Widget):
    def __init__(self, name, images, pos, container=None):
        Widget.__init__(self, container)
        self.images = images
        self.name = name
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft  = pos
        self.clickEvent = False
        self.checked = False
        self.font = pygame.font.Font(os.path.join('data','vera.ttf'),14)
        self.text = self.font.render(name,1,BLACK,WHITE)
        self.text_rect = self.text.get_rect()
        x,y,w,h = self.rect
        self.text_rect.topleft = x+w+5,y


    def move(self, pos):
        self.rect.center  = pos

    def update(self,screen):
        if self.clickEvent:
            self.clickEvent=False
        self.draw(screen)

    def click(self):
        #self.cambios = True
        self.clickEvent = True
        

    def isChecked(self):
        return self.checked 

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text,self.text_rect)
        
        
    def notify(self, event, button):
        #key = event.keyState()
        #mouse_button = event.mouseState()            
        mouse_pos = event.mousePos()
        if button == 1 and self.focused and self.checked:
            self.checked = False
            self.image = self.images[0]
            print 'uncheck'
        elif button == 1 and self.focused and not self.checked:
            self.checked = True
            self.image = self.images[1]
            print 'check'
        elif self.rect.collidepoint(mouse_pos):
            self.focused = True
        else:
            self.focused = False



#===================================================================================
#                               FUNCION PRINCIPAL
#===================================================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((200,200),16)
    back = pygame.Surface(screen.get_size(),16)
    ##color = (238,238,230)
    color = (255,255,255)
    back.fill(color)
    screen.blit(back,(0,0))

    clock = pygame.time.Clock()
    
    MyEvent = Event()


    images = []
    images.append(load_image(os.path.join('data'),'check_no.png'))
    images.append(load_image(os.path.join('data'),'check_yes.png'))

    checkbox = CheckBox('Check me',images,(100,50))

    

    while 1:
        button = 0
        
        clock.tick(40)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                button = event.button
                
        checkbox.notify(MyEvent, button)
        checkbox.update(screen)

        pygame.display.flip()



if __name__ == '__main__':
    main()
    
