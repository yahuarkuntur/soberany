import pygame
from pygame.locals import *

from xml.dom import minidom

from gui.button import Button
from gui.label import Label
from gui.textfield import TextField
from gui.checkbox import CheckBox
from gui.event import Event
from gui.utils import *


def main():

    # parse Profile XML
    doc = minidom.parse('profile.xml')
    rootNode = doc.documentElement
    player_name = rootNode.getAttribute('player')
    print 'Player:', player_name

    lang = 'english' # default languaje
    settings = []
    for setting in rootNode.getElementsByTagName('setting'):
        settings.append(setting.getAttribute('value'))
    lang = settings[0]

    # parse Translations XML
    doc = minidom.parse('language.xml')
    rootNode = doc.documentElement
    author = rootNode.getAttribute('author')
    print 'Translation author:', author

    butt_labels = []
    for language in rootNode.getElementsByTagName('language'):
        if language.getAttribute('type') == lang:
            for string in language.getElementsByTagName('string'):
                print string.getAttribute('data')
                butt_labels.append(string.getAttribute('data'))
                
    pygame.init()
    screen = pygame.display.set_mode((640,480),16)
    back = load_image(os.path.join('gui','data'),'back.png')
    screen.blit(back,(0,0))

    clock = pygame.time.Clock()
    
    MyEvent = Event()

##    cb_images = []
##    cb_images.append(load_image(os.path.join('data'),'checkbox_off.png'))
##    cb_images.append(load_image(os.path.join('data'),'checkbox_on.png'))

    b_images = []
    b_images.append(load_image(os.path.join('gui','data'),'button_off2.png'))
    b_images.append(load_image(os.path.join('gui','data'),'button_on2.png'))

    cmdNewGame = Button(butt_labels[0],b_images,(320-110,300))
    cmdLoadGame = Button(butt_labels[1],b_images,(320+10,300))
    cmdOptions = Button(butt_labels[2],b_images,(320-110,350))
    cmdCredits = Button(butt_labels[3],b_images,(320+10,350))
    cmdQuit = Button(butt_labels[4],b_images,(320-50,400))

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
