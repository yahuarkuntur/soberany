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
        

import pygame
from pygame.locals import *

class SelectionBox:
    def __init__(self):
        self.ready = False
               
    def Start(self,pos):
        self.x,self.y = pos
        self.rect = pygame.Rect(self.x,self.y,(pos[0]-self.x),(pos[1]-self.y))
        self.rects = []
        for x in range(4):
            self.rects.append(pygame.Rect(self.x,self.y,0,0))
        self.pos = pos
        self.ready = True

       
    def Show(self,pos,screen,back):
        if not self.ready:
            return
##        if self.pos == pos:
##            pygame.display.update(self.rects)
##            return
        self.Erase(screen,back)
        dx,dy = pos
        self.rects[0] = pygame.draw.line(screen,(0,255,0),(self.x,self.y),(dx,self.y),1)
        self.rects[1] = pygame.draw.line(screen,(0,255,0),(dx,self.y),(dx,dy),1)
        self.rects[2] = pygame.draw.line(screen,(0,255,0),(dx,dy),(self.x,dy),1)
        self.rects[3] = pygame.draw.line(screen,(0,255,0),(self.x,self.y),(self.x,dy),1)
        width = (dx-self.x)
        height = (dy-self.y)
        self.rect = pygame.Rect(self.x,self.y,width,height)
        if width < 0 or height < 0:
            self.rect.normalize()
##        pygame.display.update(self.rects)
        self.pos = pos


    def Erase(self,screen,back):
        if not self.ready:
            return
        for x in self.rects:
            screen.blit(back,x,x)
##        pygame.display.update(self.rects)

    def Clear(self):
        self.ready = False


    def getRect(self):
        if self.ready:
            return self.rect
        else:
            return None
            
