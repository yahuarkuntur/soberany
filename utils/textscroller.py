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

from string import splitfields

import sys

class TextScroller(pygame.sprite.Sprite):
    def __init__(self,text,back,font,posxy=(180,260),fps = 20,w = 290, h = 180):
        pygame.sprite.Sprite.__init__(self)
        if sys.platform.lower().find('win') != -1:
            # running windows
            self.text = splitfields(text,"\n")
        else:
            # linux or mac
            self.text = splitfields(text,"\r\n")
        self.font =  font#pygame.font.Font(None,20)
        self.image = pygame.Surface((w,h))
        self.image.fill((0,0,0))
        self.background = pygame.Surface((w,h))
        self.rect = self.image.get_rect().move(posxy)
        self.background.blit(back,(0,0),self.rect)
        self.pos = h
        self._delay = 1000 / fps
        self._last_update = 0
        
    def update(self,t):
        if t - self._last_update > self._delay:
            self.pos -= 1
            self.image.blit(self.background,(0,0))
            if self.pos <= len(self.text)*-15:
                self.kill()
            y = 0
            for text in self.text:
                surf = self.font.render(text,1,(255,255,255))
                rect = surf.get_rect()
                rect.topleft = 10,self.pos+15*y
                self.image.blit(surf,rect)
                y += 1
            self._last_update = t





