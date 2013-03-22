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

MAX_MESSAGES = 5

class TextSprite:
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()

    def update(self,pos):
        self.rect.topleft = pos

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def clear(self, screen, back):
        screen.blit(back,self.rect,self.rect)


class Message:
    def __init__(self,font,pos,color,screen,back):
        self.queue = []
        self._delay = 3*1000 # secs
        self._last_update = 0
        self.pos = pos
        self.font = font
        self.color = color
        self.screen = screen
        self.back = back

    def removeFirst(self):
        if len(self.queue):
            self.queue.pop(0)

    def update(self,t):
        if t - self._last_update > self._delay:
            # remove a message
            self.removeFirst()
            self._last_update = t

    def clear(self):
        for s in self.queue:
            s.clear(self.screen,self.back)
            

    def draw(self):
        x,y = self.pos
        for s in self.queue:
            s.rect.topleft = x,y
            y += 18
            s.draw(self.screen)
            

    def add(self,text):
        if len(self.queue) < MAX_MESSAGES:
            self.queue.append(TextSprite(self.font.render(text,1,self.color)))
        else:
            self.removeFirst()
            self.queue.append(TextSprite(self.font.render(text,1,self.color)))
     
