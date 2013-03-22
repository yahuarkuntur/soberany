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
        

from settings import *

from engine2d import Point



#-------------------------------------------------------------------------------
class PriorityQueue:
    def __init__(self):
        self.list = []
        self.items = 0

    def add(self,node):
        cont = 0
        for x in self.list:
            if node.f > x.f:
                cont += 1
            else:
                break
        self.list.insert(cont,node)
        self.items += 1

    def remove(self, node):
        self.list.remove(node)
        self.items -= 1

    def isEmpty(self):
        if self.items == 0:
            return True
        return False

    def pop(self):
        x = self.list.pop(0)
        self.items -= 1
        return x

#-------------------------------------------------------------------------------
class Node:
    def __init__(self):
        self.x, self.y = 0,0
        self.f = None
        self.g = None
        self.h = None
        self.parent = None

    def __init__(self,x,y):
        self.x, self.y = x,y
        self.f = None
        self.g = None
        self.h = None
        self.parent = None

    def calcF(self):
        self.f = self.g + self.h

    def getPoint(self):
        return Point(self.x, self.y)


#============================================================================================================
class PathFinder:
    def __init__(self,map,unit,start, end):
        self.map = map
        self.unit = unit
        self.start_pos = start
        self.end_pos = end

    def start(self):
        path = self.getPath(self.start_pos, self.end_pos)       
        if path and self.unit:
            print 'path asignado a',self.unit.type, self.unit.rank
            self.unit.path = path
        else:
            print "No path found"

    #------------------------------------------------------------------------------------------------
    def getPath(self,inicio,fin):
        # crear nodo inicial
        s = Node(inicio.x,inicio.y)
        s.g = 0
        s.h = self.heuristic(inicio, fin)
        s.f = s.h + s.g
        s.parent = None 
        # ingresamos el nodo inicial a Open
        open = PriorityQueue()
        open.add(s)
        closed = []
        while not open.isEmpty():
            # sacamos el nodo con F mas bajo
            actual = open.pop()
            # agregamos a la lista cerrada
            closed.append(actual)
            if actual.x == fin.x and actual.y == fin.y:
                # path encontrado
                return self.constructPath(closed)
            for vecino in self.getNeighbors(actual):
                vecino.parent = actual
                vecino.g = actual.g + self.cost(actual,vecino)
                vecino.h = self.heuristic(vecino.getPoint(),fin)
                vecino.calcF()
                
                if not self.contains(closed,vecino):
                    if not self.contains(open.list,vecino):
                        open.add(vecino)
                    else:
                        #Un coste G menor significa que este es un mejor camino.
                        old = self.getNode(open.list,vecino)
                        newg = actual.g + self.cost(actual,vecino)
                        if newg <= old.g:
                            old.parent = actual
                            old.g = newg
                            old.calcF()
        print "Path no encontrado, open vacia"
        return None
    
    #------------------------------------------------------------------------------------------------ 
    def heuristic(self,start,end):
        # Manhattan distance
        return (abs(end.x-start.x) + abs(end.y-start.y))*10
        
    def cost(self,actual, dest):
        if dest.x > actual.x:
            # esta a la derecha
            if dest.y == actual.y:
                return 10
            elif ( (dest.y > actual.y) or (dest.y < actual.y)):
                return 14 
        elif (dest.x < actual.x):
            # esta a la izq
            if (dest.y == actual.y):
                return 10
            elif ( (dest.y > actual.y) or (dest.y < actual.y)):
                return 14
        # esta en el centro
        return 10 

    def contains(self,list, node):
        if len(list) == 0:
            return False
        for i in list:
            if i.x == node.x and i.y == node.y:
                return True
        return False

    def getNode(self,list,node):
        for i in list:
            if i.x == node.x and i.y == node.y:
                return i
        return None

    def constructPath(self,list):
        aux = []
        act = list[-1]
        while act != None:
            aux.append(act)
            act = act.parent
        aux.reverse()
        return aux

    def getNeighbors(self, n):
        aux = []
        if (n.x + 1 < WIDTH and n.y <= HEIGHT):
            if (self.map[n.x + 1 + n.y*WIDTH] in WATERTILES):
                aux.append(Node(n.x + 1, n.y))
        if (n.x + 1 < WIDTH and n.y + 1 < HEIGHT):
            if (self.map[n.x + 1 + n.y*WIDTH + 1] in WATERTILES):
                aux. append(Node(n.x + 1, n.y + 1))
        if (n.x <= WIDTH and n.y + 1 < HEIGHT):
            if (self.map[n.x + n.y*WIDTH + 1] in WATERTILES):
                aux.append(Node(n.x, n.y + 1))
        if (n.x - 1 >= 0 and n.y + 1 < HEIGHT):
            if (self.map[n.x - 1 + n.y*WIDTH + 1] in WATERTILES):
                aux.append(Node(n.x - 1, n.y + 1))
        if (n.x - 1 >= 0 and n.y <= HEIGHT):
            if (self.map[n.x - 1 + n.y*WIDTH] in WATERTILES):
                aux.append(Node(n.x - 1, n.y))
        if (n.x - 1 >= 0 and n.y - 1 >= 0):
            if (self.map[n.x - 1 + n.y*WIDTH - 1] in WATERTILES):
                aux.append(Node(n.x - 1, n.y - 1))
        if (n.x <= WIDTH and n.y - 1 >= 0):
            if (self.map[n.x + n.y*WIDTH - 1] in WATERTILES):
                aux.append(Node(n.x, n.y - 1))
        if (n.x + 1 < WIDTH  and n.y - 1 >= 0):
            if (self.map[n.x + 1 + n.y*WIDTH - 1] in WATERTILES):
                aux.append( Node(n.x + 1, n.y - 1))
        return aux 


