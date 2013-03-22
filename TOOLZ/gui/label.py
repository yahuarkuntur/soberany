import pygame
from pygame.locals import *

import widget
from widget import *

import event
from event import *

import utils
from utils import *

class Label(Widget):
    def __init__(self, name, pos, image = None, container = None):
        Widget.__init__(self, container)
        self.font = pygame.font.Font(os.path.join('data','vera.ttf'), 14)
        self.name  = name
        self.text = self.font.render(self.name, 1,(0,0,0),(255,255,255))
        self.image = image
        if self.image is not None:
            self.rect = self.image.get_rect()
        else:
            self.rect = self.text.get_rect()
        self.rect.topleft = pos

    def setText(self, name):
        self.name  = name
        self.text = self.font.render(self.name, 1,(0,0,0),(255,255,255))
        self.changed = True

    def move(self, pos):
        self.rect.center = pos
        self.changed = True           

    def setImage(self, image):
        self.image = image
        self.changed = True

    def update(self,screen):
        if not self.changed:
            return
        self.text = self.font.render(self.name, 1,(0,0,0),(255,255,255))
        self.draw(screen)               

    def draw(self,screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        rect = self.text.get_rect()
        rect.center = self.rect.center
        screen.blit(self.text, rect)
          
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
    images.append(load_image(os.path.join('data'),'button.png'))
    images.append(load_image(os.path.join('data'),'button_pressed.png'))
    images.append(load_image(os.path.join('data'),'button_pressed.png'))

    label = Label('Hola ...',(100,50))


    while 1:
        clock.tick(40)

        #label.notify(MyEvent)
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

##        if label.isClicked():
##            pass

        label.update(screen)

        pygame.display.flip()
        


if __name__ == '__main__':
    main()
    
        


