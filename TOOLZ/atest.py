#! usr/bin/python

import pygame
from pygame.locals import *

import time
from time import *

import Utils.fragata
from Utils.fragata          import Fragata

import Utils.path
from Utils.path import PathFinder



tile_size = 30

def drawGrid(buffer):
    for y in range(50):
        for x in range(50):
            pygame.draw.line(buffer,(255,255,255),(x*tile_size,0),(x*tile_size,600),1)
            pygame.draw.line(buffer,(255,255,255),(0,y*tile_size),(600,y*tile_size),1)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def findPath(map,unit,start,dest):
    pathfinder = PathFinder(map,unit,start,dest)
    print 'Pathfinder starting...'
    start = time()
    pathfinder.start()
    print 'elapsed =',time()-start

def showPath(buffer,unit,surf,surf2):
##    for p in unit.path[1]:
##        f = gfont.render(str(p.f),1,(255,255,255))
##        g = gfont.render(str(p.g),1,(255,255,255))
##        h = gfont.render(str(p.h),1,(255,255,255))
##        buffer.blit(surf2,(p.x*tile_size, p.y*tile_size))
##        buffer.blit(f,(p.x*tile_size+2, p.y*tile_size+2))
##        buffer.blit(g,(p.x*tile_size+2, p.y*tile_size+tile_size-15))
##        buffer.blit(h,(p.x*tile_size+tile_size-15, p.y*tile_size+tile_size-15))
    for p in unit.path:
        f = gfont.render(str(p.f),1,(255,255,255))
        g = gfont.render(str(p.g),1,(255,255,255))
        h = gfont.render(str(p.h),1,(255,255,255))
        buffer.blit(surf,(p.x*tile_size, p.y*tile_size))
        buffer.blit(f,(p.x*tile_size+2, p.y*tile_size+2))
        buffer.blit(g,(p.x*tile_size+2, p.y*tile_size+tile_size-15))
        buffer.blit(h,(p.x*tile_size+tile_size-15, p.y*tile_size+tile_size-15))

def main():
    pygame.init()
    screen = pygame.display.set_mode((600,600),16)
    pygame.display.set_caption('A* testing')
    back = pygame.Surface(screen.get_size(),16)
    back.fill((0,0,0))
    back.convert()
    

    square = pygame.Surface((tile_size,tile_size),16)
    square.fill((0,0,255))
    square.convert()

    square2 = pygame.Surface((tile_size,tile_size),16)
    square2.fill((255,0,0))
    square2.convert()

    square3 = pygame.Surface((tile_size,tile_size),16)
    square3.fill((0,255,0))
    square3.convert()

    square4 = pygame.Surface((tile_size,tile_size),16)
    square4.fill((255,255,255))
    square4.convert()
    

    
    

    map = []

    for x in range(100*100):
        map.append(0)

    map[7+9*100] = 1
    map[7+10*100] = 1
    map[7+11*100] = 1

    back.blit(square3,(5*tile_size,10*tile_size))
    back.blit(square4,(7*tile_size,9*tile_size))
    back.blit(square4,(7*tile_size,10*tile_size))
    back.blit(square4,(7*tile_size,11*tile_size))
    

    drawGrid(back)
    screen.blit(back,(0,0))

    unit = Fragata(0)
    unit.pos = (5,10)

    font = pygame.font.Font(None,25)

    global gfont
    gfont = pygame.font.Font(None,12)
    

    while 1:
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    screen.blit(back,(0,0))
                    px,py = pygame.mouse.get_pos()
                    dest = Point(px/tile_size,py/tile_size)
                    start = Point(unit.pos[0],unit.pos[1])
                    findPath(map,unit,start,dest)
                    showPath(screen,unit,square,square2)
                    
        px,py = pygame.mouse.get_pos()
        surf = font.render(str(px/tile_size)+' , '+str(py/tile_size),1,(0,255,0))
        rect = surf.get_rect().move(5,5)
        screen.blit(surf,rect)

        pygame.display.flip()

        screen.blit(back,rect,rect)


if __name__ == '__main__':
    main()
    
