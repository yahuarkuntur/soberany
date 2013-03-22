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
from textscroller import TextScroller
from pygame.locals import *

class MisionObjectives:
    def __init__(self,misionfile,screen,back,font):
        file = open(misionfile,'r')
        self.font = font
        self.screen = screen
        self.back = back
        self.text = file.read()
        file.close()
        self.screen.blit(self.back,(0,0))
        pygame.display.flip()

    def ShowMision(self):
        mision = pygame.sprite.RenderUpdates(TextScroller(self.text,self.back, self.font))
        while 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return
                
            mision.update(pygame.time.get_ticks())
            rectlist = mision.draw(self.screen)
            pygame.display.update(rectlist)
            mision.clear(self.screen,self.back)

            if not mision:
                surf = self.font.render("-- Fin de la transmision --",1,(255,255,255))
                rect = surf.get_rect()
                rect.center = 320,260+90
                self.screen.blit(self.back,rect,rect)
                self.screen.blit(surf,rect)
                pygame.display.update(rect)
