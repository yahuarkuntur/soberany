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

RED = (255,0,0)
GREEN = (0,255,0)
ORANGE = (255,100,0)


class LifeBar(pygame.sprite.Sprite):
    def __init__(self,unit):
        pygame.sprite.Sprite.__init__(self)
        self.unit = unit
        self.color = GREEN
        self.life = self.unit.armor
        self.image = pygame.Surface((self.life/5,5),16)
        self.image.fill(self.color)
        self.image.convert()
        self.rect = self.image.get_rect()
        #self.update()

    def update(self):
        if self.unit.armor <= 0:
            self.kill()
            return

        if self.life != self.unit.armor:
            self.life = self.unit.armor
            if self.life*100/self.unit.armor2*1.0 <= 50:
                self.color = RED
            elif self.life*100/self.unit.armor2*1.0 <= 75:
                self.color = ORANGE
            else:
                self.color = GREEN
            # must be a better way!!!!
            self.image = pygame.Surface((self.life/5,5),16)
            self.image.fill(self.color)
            self.image.convert()
            self.rect = self.image.get_rect()
        else:
            x,y = self.unit.rect.center
            self.rect.center = x, y + 32
        
        
        
    
