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


from unit import Unit
from common import *


class Soberany(Unit):
    def __init__(self, uid, pos, images):
        Unit.__init__(self, pos, images, 1000, 0, 500, uid, ALMI, SUBM, 10)

class Fragata(Unit):
    def __init__(self, uid, pos, images):
        Unit.__init__(self, pos, images, 500, 15, 20, uid, CPFG, FRAG, 10)

class Misilera(Unit):
    def __init__(self, uid, pos, images):
        Unit.__init__(self, pos, images, 300, 25, 25, uid, CPNV, MISI, 10)

class Corbeta(Unit):
    def __init__(self, uid, pos, images):
        Unit.__init__(self, pos, images, 400, 15, 15, uid, CPCB, CORB, 10)

class Auxiliar(Unit):
    def __init__(self, uid, pos, images):
        Unit.__init__(self, pos, images, 250, 0, 0, uid, SUBP, AUXI, 10)

class Submarino(Unit):
    def __init__(self, uid, pos, images):
        Unit.__init__(self, pos, images, 200, 0, 25, uid, SUMA, SUBM, 10)

class GuardaCosta(Unit):
    def __init__(self, uid, pos, images):
        Unit.__init__(self, pos, images, 100, 10, 10, uid, SGOP, GUAR, 10)

class Aeronave(Unit):
    def __init__(self, uid, pos, images):
        Unit.__init__(self, pos, images, 50, 0, 0, uid, CBOP, AERO, 10)

    
        
