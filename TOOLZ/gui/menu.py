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
    b_images.append(load_image(os.path.join('data'),'button_off2.png'))
    b_images.append(load_image(os.path.join('data'),'button_on2.png'))

    cmdNewGame = Button('New Game',b_images,(320-110,300))
    cmdLoadGame = Button('Load Game',b_images,(320+10,300))
    cmdOptions = Button('Options',b_images,(320-110,350))
    cmdCredits = Button('Credits',b_images,(320+10,350))
    cmdQuit = Button('Quit',b_images,(320-50,400))

    buttons = [cmdNewGame,cmdLoadGame,cmdOptions,cmdCredits,cmdQuit]
    

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

        if cmdQuit.isClicked():
            return

        pygame.display.flip()



if __name__ == '__main__':
    main()
