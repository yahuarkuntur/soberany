import pygame
from pygame.locals import *

from button import Button
from label import Label
from textfield import TextField
from checkbox import CheckBox

from event import Event

from utils import *


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


    cb_images = []
    cb_images.append(load_image(os.path.join('data'),'checkbox_off.png'))
    cb_images.append(load_image(os.path.join('data'),'checkbox_on.png'))

    b_images = []
    b_images.append(load_image(os.path.join('data'),'button_off.png'))
    b_images.append(load_image(os.path.join('data'),'button_on.png'))

    checkbox = CheckBox('Check me',cb_images,(10,40))
    button = Button('Click me',b_images,(10,80))
    label = Label('Hola ...',(10,120))
    textbox = TextField('',100,(10,160))

    

    while 1:
        btn = 0
        key = 0
        
        clock.tick(40)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                else:
                    key = event.key
            elif event.type == MOUSEBUTTONDOWN:
                btn = event.button
                
        checkbox.notify(MyEvent, btn)
        button.notify(MyEvent)
        textbox.notify(MyEvent, key)
        
        label.update(screen)
        button.update(screen)
        textbox.update(screen)
        checkbox.update(screen)

        pygame.display.flip()



if __name__ == '__main__':
    main()
