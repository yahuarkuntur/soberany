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
        


class BasicUnit:
    def __init__(self, armor, air_damage, damage, uid, rank, utype, urange):
        self.armor = armor              # hit points
        self.air_damage = air_damage    # damage to air unit
        self.damage = damage            # damage to any water unit
        self.id = uid                   # unit unique id
        self.rank = rank                # unit rank [capitan,sarg,...]
        self.type = utype               # unit type [fragata,corbeta...]
        self.group = -1                 # unit group
        self.attack_range = urange      # unit attack range
        self.armor2 = armor             # unit armor backup
