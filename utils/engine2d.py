##         _____  _____   ____   ____   ____    __     _   _  __  __
##        / ___/ /  _  \ | __ | | ___| | __ |  /  \   |  \| | \ \/ /
##        \___ \ | |_| | | __ | | __|  |   \  / /  \  | |   |  \  /
##        /____/ \_____/ |____| |____| |_|\_\/_/  \_\ |_| \_|  |__|
##
##                           TU PAIS TE NECESITA
##        SOBERANY - A Free & Simple Real Time Strategy Game
##                              
##        (c) Copyright 2004-2006 by Brian Debuire
##
## SOBERANY is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
        

import pygame,os
from pygame.locals import *

##import xml.dom
##from xml.dom import minidom

from settings import *

import map
from map import Map

import random
from random import randint

import cPickle


def loadTiles(filename):
    print 'Loading ',filename,
    surf = load_image(filename,(255,255,255))
    w,h = surf.get_size()
    tiles = []
    for j in range(0,h,32):
        for i in range(0,w,32):
            temp_surf = surf.subsurface((i,j,32,32))
            temp_surf.convert()
            tiles.append(temp_surf)
    print 'OK'        
    return tiles

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self,p):
        if p.x == self.x and self.y == p.y:
            return True
        return False

#==============================================================================

def isAlpha(image,rect,pos):
    x,y = pos[0] - rect.left, pos[1] - rect.top
    if image.get_at((x,y)) == image.get_colorkey():
        return True
    return False

def load_font(dir,name):
    try:
        fullname = os.path.join(dir,name)
    except pygame.error, message:
        print "Unable to load font :",fullname
        raise SystemExit, message
    return fullname

# FROM THE PYGAME WIKI: modified to fit my needs ;)
# all objects must have a rect attribute and a hitmask attribute.
# The hitmask can be any pygame.surfarray array but most likely you will use
# pygame.surfarray.array_alpha(image) or pygame.sufarray.array_colorkey(image)
def pp_collide(sel_rect,unit):
    """If the function finds a collision it will return True
    if not it will return False.
    """
    rect2 = unit.rect
    hitmask = unit._hitmasks[unit.facing]

    if not sel_rect.colliderect(rect2):
##        print 'Rects dont collide'
        return False                     
    rect = sel_rect.clip(rect2)
    x2, y2 = rect.x-rect2.x, rect.y-rect2.y
    y = 0
    x = 0
    half_height = rect.height
##    half_height = rect.height/2
    while 1:
        if hitmask[x+x2][y+y2]:
##            print 'Collision at top'
            return True
##        if hitmask[x2-x][y2-y]:
##            print 'Bottom collision'
##            return True
        x += 1
        if x >= rect.width:
            x = 0
            y += 1
            if y >= half_height:
##                print 'Collision height overlap'
                return False

def load_image(name, colorkey=None):
    #fullname = os.path.join(dir, name)
    print 'loading',name
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Engine2D ERROR: Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

#==============================================================================

class Engine2D:
    def __init__(self,images):
        self.images = images
        self.offx = 0
        self.offy = 0
        self.map = None
##        self.all_units = []
        
    def drawMap(self,offx,offy,buffer):
        self.offx,self.offy = offx,offy
        for y in range(offy,screen_h+offy,1):
            for x in range(offx,screen_w+offx,1):
                buffer.blit(self.images[self.map.data[x+y*WIDTH]],((x-offx)*tile_size,(y-offy)*tile_size))

##    def getOffset(self):
##        return (self.offx)*tile_size,(self.offy)*tile_size

    def screenToMap(self,pos):
        x,y = pos
        return x/tile_size + self.offx, y/tile_size + self.offy

    def mapToScreen(self,mx,my):
        return mx*tile_size+half_tile_size, my*tile_size+half_tile_size

    def createMap(self,tile):
        self.map = Map('Default Map',WIDTH,HEIGHT)
        print self.map.name
        print self.map.width
        print self.map.height
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.map.data.append(tile)
                
    def createRandomMap(self):
        self.map = Map('Default Map',WIDTH,HEIGHT)
        print self.map.name
        print self.map.width
        print self.map.height
        for y in range(HEIGHT):
            for x in range(WIDTH):
                tile = randint(0,3)# [0,1,2,3] WATERTILES
                self.map.data.append(tile)

    def isWalkable(self,pos):
        x,y = pos
        if x >= WIDTH or y >= HEIGHT:
            print 'Coord out of bounds'
            return False
        if self.map.data[x+y*WIDTH] in WATERTILES:
            # if is water
            return True
##            for unit in self.all_units:
##                ux, uy = unit.pos
##                if ux != x and uy != y:
##                    return True
##                else:
##                    print 'Unit already in pos'
##                    return False
        return False
            
    def setTile(self,offx,offy,pos,tile_type,screen):
        # what tile we are on
        tilex,tiley = pos
        tilex = tilex/tile_size
        tiley = tiley/tile_size
        self.map.data[(tilex+offx)+(tiley+offy)*WIDTH] = tile_type
        return tilex+offx,tiley+offy

    def saveMap(self, filename):
        cPickle.dump(self.map, open(os.path.join('maps','scenario',filename+'.dat'), "wb"), 1)
    

##    def saveMap(self, filename):
##        ## a hand-made XML file
##        f = open(os.path.join('maps','scenario',filename+'.xml'),"w")
##        f.write(str('<?xml version="1.0" encoding="iso-8859-1"?>')+'\r\n')
##        f.write(str('<map name = "new map" width = "100" height = "100">')+'\r\n')
##        for data in self.map.data:
##            f.write(str('\t<tile type = "'+str(data)+'"/>')+'\r\n')
##        f.write(str('</map>'))
##        f.close()
                
    def openMap(self, filename):
        map = cPickle.load(open(os.path.join('maps','scenario',filename+'.dat')))
        self.map = map

##    def openMap(self, filename):
##        ## this way is much slower than using cPickle, but
##        ## i like this better.
##        print 'Parsing DOM tree'
##        doc = minidom.parse(filename)
##        rootNode = doc.documentElement
##        name = rootNode.getAttribute('name')
##        w = rootNode.getAttribute('width')
##        h = rootNode.getAttribute('height')
##        data = []
##        print 'Loading map...',
##        for tile in rootNode.getElementsByTagName('tile'):
##            data.append(int(tile.getAttribute('type')))
##        self.map = Map(name,w,h)
##        self.map.data = data
##        print '[OK]'

        
    def setFocus(self,pos):
        offx,offy = pos
        if offx <= half_screen_w:
            offx = 0
        elif offx >= WIDTH-half_screen_w:
            offx = WIDTH-screen_w
        else:
            offx -= half_screen_w 
        if offy <= half_screen_h:
            offy = 0
        elif offy >= HEIGHT-half_screen_h:
            offy = HEIGHT-screen_h
        else:
            offy -= half_screen_h  
        
        return offx,offy

    def getExpandedPoint(self,point):
        nuevo = Point(point.x, point.y)
        if self.isWalkable((point.x, point.y)):
            return nuevo
        s=0
        ## TODO: Validate new coords to be inside map
        while 1: 
            s += 1
            if self.isWalkable((point.x+s,point.y)):
                nuevo = Point(point.x+s, point.y)
                break
            elif self.isWalkable((point.x+s,point.y+s)):
                nuevo = Point(point.x+s, point.y+s)
                break
            elif self.isWalkable((point.x,point.y+s)):
                nuevo = Point(point.x, point.y+s)
                break
            elif self.isWalkable((point.x-s,point.y+s)):
                nuevo = Point(point.x-s, point.y+s)
                break
            elif self.isWalkable((point.x-s,point.y)):
                nuevo = Point(point.x-s, point.y)
                break
            elif self.isWalkable((point.x-s,point.y-s)):
                nuevo = Point(point.x-s, point.y-s)
                break
            elif self.isWalkable((point.x,point.y-s)):
                nuevo = Point(point.x, point.y-s)                    
                break
            elif self.isWalkable((point.x+s,point.y-s)):
                nuevo = Point(point.x+s, point.y-s)                    
                break
        return nuevo
#----------------------------------------------------------------------------------------------------------------------------  
class MiniMap:
    def __init__(self,w,h,x,y,sw,sh):
        self.image = pygame.Surface((w,h),16)
        self.image.fill((0,0,0))
        self.image.convert()
        self.rect = self.image.get_rect().move(x,y)
        self.mini_screen = pygame.Rect(x,y,sw,sh)
        self.back_image = pygame.Surface((w,h),16)
        self.back_image.convert()
        self.frame = pygame.Surface((w+4,h+4),16)
        self.frame.fill((255,255,255))
        self.frame.convert()
        self.frame_rect = self.frame.get_rect().move(x-2,y-2)
    
    def drawMiniMap(self,Xoff,Yoff,screen):
        self.mini_screen.topleft = self.rect.left+Xoff,self.rect.top+Yoff
        screen.blit(self.frame,self.frame_rect)
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,(255,255,255),self.mini_screen,1)

    def initMiniMap(self):
        for y in range(self.rect.height):
            for x in range(self.rect.width):
                self.image.set_at((x,y),(0,0,0))

    def setMiniMap(self,data,tiles,screen):
        for y in range(self.rect.height):
            for x in range(self.rect.width):
                color = tiles[data[x+y*WIDTH]].get_at((16,16))
                self.image.set_at((x,y),color)
        self.back_image.blit(self.image,(0,0))
        screen.blit(self.image,self.rect)

    def refresh(self):
        self.image.blit(self.back_image,(0,0))

    def setTile(self,x,y,tile):
        color = tile.get_at((16,16))
        self.image.set_at((x,y),color)

    def drawMiniUnit(self,x,y,image,screen):
        screen.blit(image,(self.rect.left+x,self.rect.top+y))
        

    def getMiniMapPos(self,pos):
        xpos,ypos = pos
        xpos = xpos - self.rect.left
        ypos = ypos - self.rect.top
        #print 'xpos,ypos',xpos,ypos
        return xpos,ypos





