# -*- coding: cp1252 -*-

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
        

# Unit types
FRAG = 'Fragata'
CORB = 'Corbeta'
MISI = 'Misilera'
AUXI = 'Auxiliar'
SUBM = 'Submarino'
GUAR = 'Guardacosta'
AERO = 'Aeronave'
##SOBE = 'Soberany - Submarino nuclear'

# Unit attack definition

attack_defs = dict(
                Fragata=[FRAG,CORB,MISI,AUXI,GUAR,SUBM],
                Corbeta=[FRAG,CORB,MISI,AUXI,GUAR],
                Misilera=[FRAG,CORB,MISI,AUXI,GUAR,SUBM,AERO],
                Auxiliar=[],
                Submarino=[FRAG,CORB,MISI,AUXI,GUAR,SUBM],
                Guardacosta=[FRAG,CORB,MISI,AUXI,GUAR,AERO],
                Aeronave=[])

# Ranks
MARO = 'Marinero'
CBOS = 'Cabo Segundo'
CBOP = 'Cabo Primero'
SGOS = 'Sargento Segundo'
SGOP = 'Sargento Primero'
SUBS = 'Suboficial Segundo'
SUBP = 'Suboficial Primero'
SUMA = 'Suboficial Mayor'
ALFG = 'Alférez de Fragata'
TNFG = 'Teniente de Fragata'
TNNV = 'Teniente de Navío'
CPCB = 'Capitán de Corbeta'
CPFG = 'Capitán de Fragata'
CPNV = 'Capitán de Navio'
CALM = 'Contralmirante'
VALM = 'Vicealmirante'
ALMI = 'Almirante'

# FSM states
IDLE = 0
WALK = 1
ATTACK = 2
FLEE = 3
##UNDER_ATTACK = 4

FSM_STATES = ['idle','walk','attack','flee']#,'under_attack']

MSG_FLEE = 0
MSG_ATTACKED = 1
MSG_KILLED = 2

# dir
EAST    = 0
SEAST   = 1
SOUTH   = 2
SWEST   = 3
WEST    = 4
NWEST   = 5
NORTH   = 6
NEAST   = 7


# turn from gamedev.net
def turn(dir, turn):
    return((dir+turn) & 7)

def getDir(start,end):
    if end.x == start.x and end.y > start.y:
        return SOUTH
    if end.x == start.x and end.y < start.y:
        return NORTH
    if end.y == start.y and end.x > start.x:
        return EAST
    if end.y == start.y and end.x < start.x:
        return WEST
    if end.x > start.x and end.y > start.y:
        return SEAST
    if end.x < start.x and end.y < start.y:
        return NWEST
    if end.x > start.x and end.y < start.y:
        return NEAST
    if end.x < start.x and end.y > start.y:
        return SWEST
    






