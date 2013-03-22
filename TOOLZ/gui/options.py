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
    screen = pygame.display.set_mode((640,480),16)
    back = load_image(os.path.join('data'),'back.png')
    screen.blit(back,(0,0))

    clock = pygame.time.Clock()
    
    MyEvent = Event()

    cb_images = []
    cb_images.append(load_image(os.path.join('data'),'checkbox_off.png'))
    cb_images.append(load_image(os.path.join('data'),'checkbox_on.png'))

    b_images = []
    b_images.append(load_image(os.path.join('data'),'button_off3.png'))
    b_images.append(load_image(os.path.join('data'),'button_on3.png'))

    lbl01 = Label('Player Name',(320-100,300+2))
    txtPlayer = TextField('',150,(320,300),15)
    cmdLoadGame = Button('Load Game',b_images,(320+10,300))
    cmdOptions = Button('Options',b_images,(320-110,350))
    
    cmdCancel = Button('Cancel',b_images,(320+10,400))
    cmdAccept = Button('Accept',b_images,(320-110,400))

    buttons = [cmdAccept,cmdCancel]
    textfields = [txtPlayer]
    labels = [lbl01]
    

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

        for button in buttons:
            button.notify(MyEvent)
            button.update(screen)

        for textfield in textfields:
            textfield.notify(MyEvent, key)
            textfield.update(screen)

            
        for label in labels:
            label.update(screen)

        if cmdCancel.isClicked():
            return

        pygame.display.flip()



if __name__ == '__main__':
    main()
