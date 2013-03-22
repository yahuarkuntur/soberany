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


def load_sound(filepath):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(filepath)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound


def playSound(sound):
    soundfx = load_sound(sound)
    soundfx.set_volume(0.4)
    channel = soundfx.play()
##    if channel:
##        channel.set_volume(0.4)


class SoundFX:
    def __init__(self):
        self.channel = None

    def update(self):
        if self.channel:
            if not self.channel.get_busy(): # still playing
                self.channel = None

    def play(self,sound):
        if not self.channel:
            soundfx = load_sound(sound)
            soundfx.set_volume(0.4)
            self.channel = soundfx.play()
##            if self.channel:
##                self.channel.set_volume(0.4)



##class BackgroundSound:
##    def __init__(self,sound):
##        self.sound = sound
##        self.channel = None
##        self.sound.set_volume(0.5)
##        
##    def update(self):
##        if self.channel:
##            if self.channel.get_busy(): # still playing
##                pass
##            else:
##                self.channel = None
##
##    def play(self):
##        if not self.channel:
##            self.Start()
##
##
##    def Start(self):
##        self.channel = self.sound.play()
        
        
