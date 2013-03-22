from xml.dom import minidom

import pygame, os
from pygame.locals import *

    
    

def main():
    doc = minidom.parse(os.path.join('misions','tutorial.xml'))
    rootNode = doc.documentElement
    misionName = rootNode.getAttribute('name')
    print 'Mision Name:', misionName

    for alliedUnit in rootNode.getElementsByTagName('allied'):
        for unit in alliedUnit.getElementsByTagName('unit'):
            print 'Allied unit:',unit.getAttribute('type')
            print 'Allied Xpos:',unit.getAttribute('x')
            print 'Allied Ypos:',unit.getAttribute('y')
            
    for enemyUnit in rootNode.getElementsByTagName('enemy'):
        for unit in enemyUnit.getElementsByTagName('unit'):
            print 'Enemy unit:',unit.getAttribute('type')
            print 'Enemy Xpos:',unit.getAttribute('x')
            print 'Enemy Ypos:',unit.getAttribute('y')

    print "-"*50

    doc = minidom.parse('language.xml')
    rootNode = doc.documentElement
    author = rootNode.getAttribute('author')
    print 'Translation author:', author

    for language in rootNode.getElementsByTagName('language'):
        if language.getAttribute('type') == "spanish":
            for string in language.getElementsByTagName('string'):
                print string.firstChild.nodeValue
                #print string.getAttribute('data')
                
    for language in rootNode.getElementsByTagName('language'):
        if language.getAttribute('type') == "english":
            for string in language.getElementsByTagName('string'):
                print string.getAttribute('data')
            




main()
    
