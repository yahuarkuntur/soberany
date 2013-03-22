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

from basicunit import BasicUnit

from common import *

from engine2d import Point

#from sprite import Sprite

from settings import *

from math import sqrt


class Unit(BasicUnit,pygame.sprite.Sprite):
    def __init__(self,pos,images,armor, air_damage, damage, uid, rank, utype, urange):
        BasicUnit.__init__(self, armor, air_damage, damage, uid, rank, utype, urange)
        pygame.sprite.Sprite.__init__(self)
        # unit vars
        self.path = None
        self.pos = pos      # position in map coords
        # finite state machine vars
        self.facing = EAST
        self.target = None
        self.state = IDLE
        self._shot_delay = 1000
        self._shot_update = 0
        self.shot = False
        self.flee_dest = -1,-1
        # sprite vars
        self._images = images
        # create hit masks for pp collision
        self.createHitMasks()
        fps = 10
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.rect = self._images[0].get_rect().move(pos)
        self.image = self._images[self.facing]

    def createHitMasks(self):
        self._hitmasks = []
        for image in self._images:
            img = image.copy()
            self._hitmasks.append(pygame.surfarray.array_colorkey(img))
        print 'hitmasks ready!'

    def getAttack(self,damage):
        # i'm recieveng damage
        if self.armor > 0:
            self.armor -= damage
            return False
        else:
            return True

    def move(self):
##        if self.path:
        next_pos = self.path[0]
        # update facing
        px,py = self.pos
        new_facing = getDir(Point(px,py),next_pos)
        if new_facing != self.facing and new_facing != None:
            self.facing = new_facing
        self.image = self._images[self.facing]
        # update pos
        self.pos = next_pos.x,next_pos.y
        del self.path[0]

    def calcPos(self,offx,offy):
        self.rect.topleft = (tile_size*(self.pos[0]-offx)-half_tile_size,tile_size*(self.pos[1]-offy)-half_tile_size)

    def attack(self):
        if not self.target:
            return
        if self.target.getAttack(self.damage):
            # Unit killed
            self.target = None
            self.state = IDLE
        else:
            self.shot = True

    
    def targetDist(self,target):
        # target pos
        tx,ty = target.pos
        # unit pos
        px,py = self.pos
        dx = abs(tx-px)
        dy = abs(ty-py)
        ### BETTER WAY????
        urange = sqrt(dx*dx + dy*dy)
        return urange

    def inAttackRange(self,unit):
        dist = self.targetDist(unit)
        if dist < self.attack_range:
            return True
        return False
        

    def searchEnemy(self,enemies):
        # find the closest enemy
        closer = 50
        self.target = None
        for e in enemies:
            dist = self.targetDist(e)
            if dist < self.attack_range:
                if dist < closer:
                    closer = dist
                    self.target = e
        if self.target != None:
            return True
        return False

    def canAttack(self):
        if self.target.type in attack_defs[self.type]:
            return True
        else:
            return False

    def canAttackMe(self):
        if self.type in attack_defs[self.target.type]:
            return True
        else:
            return False


    def setState(self,state):
        self.state = state


    def update(self,t,offx,offy,enemies):
        self.calcPos(offx,offy)
        ######################## W A L K
        if self.state == WALK:
            if t - self._last_update > self._delay:
                self._last_update = t
                if self.path:
                    self.move()
                else:
                    self.setState(IDLE)
        ######################### A T T A C K
        elif self.state == ATTACK:
            if t - self._shot_update > self._shot_delay:
                self._shot_update = t
                if not self.inAttackRange(self.target) and self.canAttack():
                    # pursuit unit !!!
                    px,py = self.target.pos
                    ux,uy = self.pos
                    dx = (ux-px)/2
                    dy = (uy-py)/2
                    x,y = ux - dx, uy - dy
                    if x >= 0 and x < 100 and y >= 0 and y < 100:
                        self.flee_dest = x,y
                    else:
                        #print 'Flee dest error',x,y
                        self.flee_dest = -1,-1
                    self.state = WALK
                else:
                    self.attack()
            else:
                self.shot = False
        ########################## F L E E
        elif self.state == FLEE:
            # flee away from target
            px,py = self.target.pos
            ux,uy = self.pos
            dx = ux-px
            dy = uy-py
            x,y = ux + dx, uy + dy
            if x >= 0 and x < 100 and y >= 0 and y < 100:
                self.flee_dest = x,y
            else:
                #print 'Flee dest error',x,y
                self.flee_dest = -1,-1
            self.state = WALK
        ######################## I D L E
        elif self.state == IDLE:
            if self.target:
                self.setState(ATTACK)
                return
            if self.searchEnemy(enemies):
                if self.canAttackMe() and not self.canAttack():
                    self.setState(FLEE)
                elif self.canAttackMe() and self.canAttack():
                    self.setState(ATTACK)
                elif not self.canAttackMe() and not self.canAttack():
                    self.setState(IDLE)
                elif not self.canAttackMe() and self.canAttack():
                    self.setState(ATTACK)

    

                               
