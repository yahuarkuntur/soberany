#! usr/bin/python
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
##
## Contact me at debuirebrian(at)gmail(dot)com

print 'Soberany version 0.2, Copyright (C) 2004-2006 by Brian Debuire'
print 'Soberany comes with ABSOLUTELY NO WARRANTY; for details see LICENSE.TXT'
print 'This is free software, and you are welcome to redistribute it'
print 'under certain conditions; see LICENSE.txt for details.'

print 'Soberany - Tu pais te necesita'
print 
import sys, platform
print '*'*80
print 'Plataforma:',platform.platform()
print 'Sistema:',platform.system()
print 'Python:',sys.version
print '*'*80
print
print 'Importando modulos',

import xml.dom
from xml.dom import minidom

import utils.engine2d
from utils.engine2d             import isAlpha, load_font, load_image, Engine2D, MiniMap, Point
print '.',
import utils.selbox
from utils.selbox               import SelectionBox
print '.',
import utils.selectedunit
from utils.selectedunit         import SelectedUnit
print '.',
import utils.settings
from utils.settings             import *
print '.',
import utils.target
from utils.target               import Target
print '.',
import utils.lifebar
from utils.lifebar               import LifeBar
print '.',
##import utils.wireframe
##from utils.wireframe        import Wireframe

import utils.sounds
from utils.sounds              import SoundFX, playSound
print '.',
import utils.message
from utils.message              import Message
print '.',
import utils.all_units
from utils.all_units            import *
print '.',
import utils.mision
from utils.mision          import MisionObjectives
print '.',
import utils.astar
from utils.astar                import PathFinder
print '.',
import utils.common
from utils.common               import *
print '.',
import utils.explosion
from utils.explosion            import Explosion
print '.',

import pygame,os
from pygame.locals import *
print '\t[OK]'
print 


class Game:
    def __init__(self):
        self.initScreen()
        self.loadMapImages()
        self.Engine2D = Engine2D(self.tiles)
        self.loadTargetImages()
        self.loadExtras()
        self.loadUnitImages()
        self.loadSoundFX()
##        self.loadSubWireframes()

    #................................................................................................        
    def initScreen(self,dim=(640,480),depth=16):
        pygame.init()
        self.screen = pygame.display.set_mode(dim,depth)
        pygame.display.set_caption('Soberany - Tu pais te necesita...')
        self.back = pygame.Surface(self.screen.get_size(),depth)
        self.back.fill((0,0,0))
        self.screen.blit(self.back,(0,0))
    #................................................................................................        
    def loadMapImages(self):
        dir = os.path.join('gfx','tiles')
        self.tiles = []
        self.tiles.append(load_image(dir,'water.gif'))
##        for x in range(1,6):
##            self.tiles.append(load_image(dir,'water0'+str(x)+'.png'))
        self.tiles.append(load_image(dir,'grass.gif'))
        self.tiles.append(load_image(dir,'desert.gif'))
        self.tiles.append(load_image(dir,'swamp.gif'))
        self.tiles.append(load_image(dir,'hill.gif'))
        self.tiles.append(load_image(dir,'rocks.gif'))
        self.tiles.append(load_image(dir,'forest.gif'))
        self.tiles.append(load_image(dir,'jungle.gif'))
    #---------------------------------------------------------------------------------------------------
    def loadMaps(self):
        #self.Engine2D.createMap(0)
        self.Engine2D.openMap(os.path.join('maps','campains','mision01.xml'))
        # Create Minimap  
        self.miniMap = MiniMap(WIDTH,HEIGHT,MINI_MAP_X,MINI_MAP_Y,screen_w,screen_h)
        self.miniMap.setMiniMap(self.Engine2D.map.data,self.tiles,self.screen)
        self.miniMap.drawMiniMap(0,0,self.screen)
    #---------------------------------------------------------------------------------------------------
    def loadTargetImages(self):
        dir = os.path.join('gfx','gui')
        self.target_images = []
        for x in range(5):
            self.target_images.append(load_image(dir,'target0'+str(x)+'.gif'))
            
    def loadUnitImages(self):
        # load unit images
        self.unit_images = []
        # fragata
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','fragata'),'fragata0'+str(x)+'.gif'))
        # corbeta
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','corbeta'),'corbeta0'+str(x)+'.gif'))
        # misilera
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','misilera'),'misilera0'+str(x)+'.gif'))
        # auxiliar
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','auxi'),'auxi0'+str(x)+'.gif'))
        # submarino
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','sub'),'sub0'+str(x)+'.gif'))
        # guardacosta
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','guarda'),'guarda0'+str(x)+'.gif'))
        # aeronave
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','nave'),'nave0'+str(x)+'.gif'))

    def loadExtras(self):
        # load panel
        self.panel = load_image(os.path.join('gfx','gui'),'panel.gif')
        self.panel_rect = self.panel.get_rect()
        self.panel_rect.centerx = 320
        self.panel_rect.bottom = 480

        # create miniunits
        self.allied_mini_unit_surf = pygame.Surface((1,1),16)
        self.allied_mini_unit_surf.fill(ALLIED_UNIT_COLOR)
        self.allied_mini_unit_surf.convert()

        self.enemy_mini_unit_surf = pygame.Surface((1,1),16)
        self.enemy_mini_unit_surf.fill(ENEMY_UNIT_COLOR)
        self.enemy_mini_unit_surf.convert()
        
        # selected unit            
        self.selected = load_image(os.path.join('gfx','unit','extras'),'selected.gif')
        # selected enemy
        self.selected2 = load_image(os.path.join('gfx','unit','extras'),'selected_enemy.gif')
        # explosions        
        self.explosion_images = []
        for x in range(1,5):
            self.explosion_images.append(load_image(os.path.join('gfx','unit','extras'),'explosion0'+str(x)+'.gif'))
        # shots
        self.shot_images = []
        for x in range(1,4):
            self.shot_images.append(load_image(os.path.join('gfx','unit','extras'),'hit0'+str(x)+'.gif'))

    def loadSoundFX(self):
        # unit sounds
        self.fragata_sounds = []
        self.fragata_sounds.append(os.path.join('sfx','fragata','fragata.death00.wav'))
        self.fragata_sounds.append(os.path.join('sfx','fragata','fragata.ready00.wav'))
        self.fragata_sounds.append(os.path.join('sfx','fragata','fragata.order00.wav'))
        self.fragata_sounds.append(os.path.join('sfx','fragata','fragata.select00.wav'))

        # weapon sounds
        self.weapon_sounds = []
        self.weapon_sounds.append(os.path.join('sfx','weapon','cannon.hit00.wav'))
        self.weapon_sounds.append(os.path.join('sfx','weapon','missile.hit00.wav'))

##    def loadSubWireframes(self):
##        dir = os.path.join('gfx','wireframes','sub')
##        self.sub_wires = []
##        for x in range(1,13):
##            if x < 10:
##                self.sub_wires.append(load_image(dir,'sub0'+str(x)+'.png',-1))
##            else:
##                self.sub_wires.append(load_image(dir,'sub'+str(x)+'.png',-1))

    def findPath(self,unit,dest):
        start = Point(unit.pos[0],unit.pos[1])
        pathfinder = PathFinder(self.Engine2D.map.data,unit,start,dest)
        print 'iniciando Pathfinder...'
        pathfinder.start()
        unit.setState(WALK)


    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # KEYBOARD HANDLING---------------------------------------------
                if event.key == K_ESCAPE:
                    return -1
                # Brian : Now when pressing Ctrl + [1,2] we create a group,
                # and when pressing [1,2] if there is a group it gets selected
                elif event.key == K_1:
                    if self.do_group:
                        self.messages.add('Asignando Grupo 1')
                elif event.key == K_2:
                    if self.do_group:
                        self.messages.add('Asignando Grupo 2')
                elif event.key == K_F10:
                     self.messages.add('-- MENU --')
                     
                elif event.key == K_F1:
                     self.messages.add('-- HELP --')
                     
            elif event.type == MOUSEBUTTONDOWN:
                # MOUSE BUTTON DOWN HANDLING
                if event.button == 1:
                    # Click on minimap!!!
                    if self.miniMap.rect.collidepoint(event.pos):
                        self.offx,self.offy = self.Engine2D.setFocus(self.miniMap.getMiniMapPos(event.pos))
                        self.dirty = True
                    else:
                        self.SelBox.Start(event.pos)
                        # if click on unit
                        self.selected_units = []
                        self.selected_enemy = None
                        self.selected_mark = pygame.sprite.RenderUpdates()
                        self.life_bars = pygame.sprite.RenderUpdates()
                        for unit in self.allied_units.sprites():
                            if unit.rect.collidepoint(event.pos) and not isAlpha(unit.image,unit.rect,event.pos):
                                self.selected_units.append(unit)
                                self.sound.play(self.fragata_sounds[3])
                                self.selected_mark.add(SelectedUnit(self.selected,unit))
                                self.life_bars.add(LifeBar(unit))
                                # show unit info
                                return 1
                        # click on enemy unit                       
                        for unit in self.enemy_units.sprites():
                            if unit.rect.collidepoint(event.pos) and not isAlpha(unit.image,unit.rect,event.pos):
                                self.selected_mark.add(SelectedUnit(self.selected2,unit))
                                self.life_bars.add(LifeBar(unit))
                                self.selected_enemy = unit
                                # show enemy info
                                return 1
                        
                elif event.button == 3:
                    # Right mouse button click
                    # if there is any unit selected... handle motion
                    if self.selected_units == []:
                        # no units selected!!!
                        return 1
                    self.sound.play(self.fragata_sounds[2])
                    # attack??? enemy unit                       
                    for unit in self.enemy_units.sprites():
                        if unit.rect.collidepoint(event.pos) and not isAlpha(unit.image,unit.rect,event.pos):
                            # enemy unit selected
                            self.selected_units[0].target = unit
                            if self.selected_units[0].canAttack():
                                self.selected_units[0].setState(ATTACK)
                            else:
                                self.messages.add('Error: '+unit.type+' enemiga no puede ser atacada.')
                                self.selected_units[0].target = None
                            return 1

                    if self.miniMap.rect.collidepoint(event.pos):
                        # minimap jump
                        x,y = self.miniMap.getMiniMapPos(event.pos)
                        dest = self.Engine2D.mapToScreen(x-self.offx,y-self.offy)
                        if not self.Engine2D.isWalkable((x,y)):
                            self.messages.add('Coordenadas inválidas en : '+str(x)+','+str(y))
                            return 1
                        self.messages.add('Coordenadas confirmadas en : '+str(x)+','+str(y))
                        self.findPath(self.selected_units[0],Point(x,y))
                        self.selected_units[0].target = None
                        if not self.target:
                            self.target.add(Target(self.target_images,dest))
                    if (self.panel_rect.collidepoint(event.pos) and isAlpha(self.panel,self.panel_rect,event.pos)) or not self.panel_rect.collidepoint(event.pos):
                        # transparent part of panel so we can move
                        x,y = self.Engine2D.screenToMap(event.pos)
                        dest = self.Engine2D.mapToScreen(x-self.offx,y-self.offy)
                        if not self.Engine2D.isWalkable((x,y)):
                            self.messages.add('Coordenadas inválidas en : '+str(x)+','+str(y))
                            return 1
                        self.messages.add('Coordenadas confirmadas en : '+str(x)+','+str(y))
                        self.findPath(self.selected_units[0],Point(x,y))
                        self.selected_units[0].target = None
                        if not self.target:
                            self.target.add(Target(self.target_images,dest))
            elif event.type == MOUSEBUTTONUP:
                # MOUSE BUTTON RELEASED HANDLING
                selection_rect = self.SelBox.getRect()
                if selection_rect:
                    pass
                self.SelBox.Erase(self.screen,self.back)
                self.SelBox.Clear()
        return 1


    def handleKeyBoard(self):
        self.k = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_button = pygame.mouse.get_pressed()
        
        if self.k[K_LEFT] or (self.mouse_pos[0] < 2 and not self.mouse_button[0]):
            if self.offx > 0:
                self.offx -= 1
                self.dirty = True
        elif self.k[K_RIGHT] or (self.mouse_pos[0] > WINDOW_W-2 and not self.mouse_button[0]):
            if self.offx < WIDTH-screen_w:
                self.offx += 1
                self.dirty = True
        elif self.k[K_UP] or (self.mouse_pos[1] < 2 and not self.mouse_button[0]):
            if self.offy > 0:
                self.offy -= 1
                self.dirty = True
        elif self.k[K_DOWN] or (self.mouse_pos[1] > WINDOW_H-2 and not self.mouse_button[0]):
            if self.offy < HEIGHT-screen_h:
                self.offy += 1
                self.dirty = True

        if self.k[K_LCTRL]:
            self.do_group = True
        else:
            self.do_group = False



    def showUnitInfo(self,unit):
        # unit type
        surf = self.font.render(''+unit.type,1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y)
        self.screen.blit(surf,rect)
        # unit rank
        surf = self.font.render(''+unit.rank,1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+12)
        self.screen.blit(surf,rect)
        # unit armor
        surf = self.font.render('Blindaje : '+str(unit.armor)+'/'+str(unit.armor2),1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+24)
        self.screen.blit(surf,rect)
        # unit damage
        surf = self.font.render('Daño : '+str(unit.damage),1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+36)
        self.screen.blit(surf,rect)
        # unit air damage
        surf = self.font.render('Daño antiaéreo : '+str(unit.air_damage),1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+48)
        self.screen.blit(surf,rect)
        # fsm info
        surf = self.font.render('Estado IA : '+FSM_STATES[unit.state],1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+60)
        self.screen.blit(surf,rect)
        

    def clearSprites(self):
        self.screen.blit(self.back,self.fps_rect,self.fps_rect)
        self.target.clear(self.screen, self.back)
##        self.wireframes.clear(self.screen, self.back)
        self.messages.clear()
        self.allied_units.clear(self.screen, self.back)
        self.enemy_units.clear(self.screen, self.back)
        self.selected_mark.clear(self.screen, self.back)
        self.explosions.clear(self.screen, self.back)
        self.shots.clear(self.screen, self.back)
        self.life_bars.clear(self.screen, self.back)

    def drawAll(self):
        ticks = pygame.time.get_ticks()
        if self.dirty:
            self.Engine2D.drawMap(self.offx,self.offy,self.back)
            self.screen.blit(self.back,(0,0))
            self.dirty = False

        # blit target sprite
        self.target.update(ticks)
        self.target.draw(self.screen)

        # blit selection marks
        self.selected_mark.update()
        self.selected_mark.draw(self.screen)

        # blit life bars
        self.life_bars.update()
        self.life_bars.draw(self.screen)

        # blit units
        self.allied_units.update(ticks,self.offx,self.offy,self.enemy_units.sprites())
        self.enemy_units.update(ticks,self.offx,self.offy,self.allied_units.sprites())
        self.allied_units.draw(self.screen)
        self.enemy_units.draw(self.screen)
        
        # blit explosions
        self.explosions.update(ticks, self.offx, self.offy)
        self.explosions.draw(self.screen)

        self.shots.update(ticks, self.offx, self.offy)
        self.shots.draw(self.screen)

        # blit Panel
        self.screen.blit(self.panel,self.panel_rect)

        # blit Mini Map
        self.miniMap.drawMiniMap(self.offx,self.offy,self.screen)

        # blit mini units
        for mu in self.allied_units.sprites():
            if mu.flee_dest != (-1,-1):
                # flee
                x,y = mu.flee_dest
                if self.Engine2D.isWalkable((x,y)):
                    print 'Destino FLEE inválido:',x,y
                    self.findPath(mu,Point(x,y))
                mu.flee_dest = -1,-1
            if mu.shot and mu.target.armor > 0:
                self.shots.add(Explosion(self.shot_images,mu.target.pos))
                # play shot sound
                playSound(self.weapon_sounds[0])
                mu.shot = False
            if mu.armor <= 0:
                self.explosions.add(Explosion(self.explosion_images,mu.pos))
                mu.kill()
                # play explosion sound
                playSound(self.fragata_sounds[0])
                self.messages.add(mu.type+'aliada destruida.')
            else:
                self.miniMap.drawMiniUnit(mu.pos[0],mu.pos[1],self.allied_mini_unit_surf,self.screen)
        for mu in self.enemy_units.sprites():
            if mu.flee_dest != (-1,-1):
                # flee
                x,y = mu.flee_dest
                if self.Engine2D.isWalkable((x,y)):
                    print 'Destino FLEE inválido:',x,y
                    self.findPath(mu,Point(x,y))
                mu.flee_dest = -1,-1
            if mu.shot and mu.target.armor > 0:
                self.shots.add(Explosion(self.shot_images,mu.target.pos))
                # play shot sound
                playSound(self.weapon_sounds[0])
                mu.shot = False

            if mu.armor <= 0:
                self.explosions.add(Explosion(self.explosion_images,mu.pos))
                mu.kill()
                # play explosion sound
                playSound(self.fragata_sounds[0])
                self.messages.add(mu.type+'enemiga destruida.')
            else:
                self.miniMap.drawMiniUnit(mu.pos[0],mu.pos[1],self.enemy_mini_unit_surf,self.screen)


        # blit some info 
        surf = self.font.render('fps = '+str(int(self.clock.get_fps())),1,UNIT_INFO_COLOR)
        self.fps_rect = surf.get_rect().move(5,5)
        self.screen.blit(surf,self.fps_rect)

        # show wireframes animation
##        self.wireframes.update(ticks)
##        self.wireframes.draw(self.screen)

        # show messages
        self.messages.update(ticks)
        self.messages.draw()

        # show unit info
        if self.selected_units != []:
            self.showUnitInfo(self.selected_units[0])
        if self.selected_enemy != None:
            self.showUnitInfo(self.selected_enemy)

        
        
    #................................................................................................        
    def setup(self):
        # Units
##        self.allied_units = pygame.sprite.RenderUpdates()
##        self.allied_units.add(Fragata(1,(80,70),self.unit_images[0:8]))
##        #self.allied_units.add(Fragata(1,(3,3),self.unit_images[0:8]))
##        self.allied_units.add(Corbeta(2,(80,72),self.unit_images[8:8*2]))
##        self.allied_units.add(Misilera(3,(80,75),self.unit_images[8*2:8*3]))
##        self.allied_units.add(Auxiliar(4,(84,73),self.unit_images[8*3:8*4]))
##        self.allied_units.add(Misilera(3,(83,75),self.unit_images[8*2:8*3]))
####        self.allied_units.add(Submarino(1,(80,15),self.unit_images[8*4:8*5]))
##        self.allied_units.add(GuardaCosta(5,(90,20),self.unit_images[8*5:8*6]))
####        self.allied_units.add(Aeronave(1,(,21),self.unit_images[8*6:8*7]))
        #self.allied_units.add(Soberany(1,(10,6),self.unit_images[24:24+8]))
##
##        # Enemy Units
##        self.enemy_units = pygame.sprite.RenderUpdates()
##        self.enemy_units.add(Misilera(1,(16,8),self.unit_images[8*2:8*3]))
##        self.enemy_units.add(Corbeta(2,(18,6),self.unit_images[8:8*2]))
##        self.enemy_units.add(Corbeta(3,(18,10),self.unit_images[8:8*2]))

        # load mision from XML
        self.loadMision(os.path.join('misions','tutorial.xml'))

        # Explosions gfx
        self.explosions = pygame.sprite.RenderUpdates()
        self.shots = pygame.sprite.RenderUpdates()

        # selection mark
        self.selected_mark = pygame.sprite.RenderUpdates()

        # life bars
        self.life_bars = pygame.sprite.RenderUpdates()

        # selected units & enemy
        self.selected_units = []
        self.selected_enemy = None
    
        self.offx = 0
        self.offy = 0

        # game font
        self.font = pygame.font.Font(load_font('fonts','vera.ttf'),10)

        # game sound engine
        self.sound = SoundFX()

        # Input & time 
        self.clock = pygame.time.Clock()
        self.k = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_button = pygame.mouse.get_pressed()

        # create Selection Box
        self.SelBox = SelectionBox()

        # Target sprite
        self.target = pygame.sprite.RenderUpdates()

##        # create wireframes
##        self.wireframes = pygame.sprite.RenderUpdates(Wireframe(self.sub_wires,(533,373)))

        # create messages
        self.messages = Message(self.font,(10,50),(0,255,0),self.screen,self.back)

        self.dirty = True

        # groups
        self.do_group = False
        # many units can belong to many groups
        self.Group1 = []
        self.Group2 = []


    def main_loop(self):

        mision_back = load_image(os.path.join('gfx','gui'),'back.png')
        title_font = pygame.font.Font(load_font('fonts','sten.ttf'),50)
        mision_font = pygame.font.Font(load_font('fonts','vera.ttf'),14)
        subt_font = pygame.font.Font(load_font('fonts','sten.ttf'),20)
        surf = title_font.render('SOBERANY',1,(255,255,255))
        rect = surf.get_rect()
        rect.center = 320,100
        mision_back.blit(surf,rect)
        mision = MisionObjectives(os.path.join('misions','intro.txt'),self.screen,mision_back,mision_font)
        mision.ShowMision()
        surf = subt_font.render('OBJETIVOS DE LA MISION',1,(0,255,0))
        rect = surf.get_rect()
        rect.center = 320,170
        mision_back.blit(surf,rect)
        mision = MisionObjectives(os.path.join('misions','mision01.txt'),self.screen,mision_back,mision_font)
        mision.ShowMision()

        # load mision map
        self.loadMaps()

        # setup initial pos
        self.offx,self.offy = self.Engine2D.setFocus((90,20))
        
        while 1:
            
            self.clock.tick(40)

            self.handleKeyBoard()

            # handle events
            if self.handleEvents() < 0:
                return

            # draw everything
            self.drawAll()

            # update sound
            self.sound.update()
            
            if self.mouse_button[0]:
                self.SelBox.Show(pygame.mouse.get_pos(),self.screen,self.back)

            # update all
            pygame.display.flip()

            # clear sprites
            self.clearSprites()

            
            if self.gameOver():
                return


    def Run(self):
        self.setup()
        self.main_loop()

    def gameOver(self):

        title_font = pygame.font.Font(load_font('fonts','sten.ttf'),50)
        if not len(self.allied_units):
            pygame.time.wait(1000)
            surf = title_font.render('MISION FALLIDA!',1,(255,0,0))
        elif not len(self.enemy_units):
            pygame.time.wait(1000)
            surf = title_font.render('MISION CUMPLIDA!',1,(0,255,0))
        else:
            return False
        rect = surf.get_rect()
        rect.center = 320,240
        self.screen.blit(surf,rect)
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return True

    def loadMision(self, filename):
        self.allied_units = pygame.sprite.RenderUpdates()
        self.enemy_units = pygame.sprite.RenderUpdates()
        doc = minidom.parse(filename)
        rootNode = doc.documentElement
        misionName = rootNode.getAttribute('name')
        print 'Mision Name:', misionName

        for alliedUnit in rootNode.getElementsByTagName('allied'):
            for unit in alliedUnit.getElementsByTagName('unit'):
                unitType = unit.getAttribute('type')
                unitID = int(unit.getAttribute('uid'))
                unitPx = int(unit.getAttribute('x'))
                unitPy = int(unit.getAttribute('y'))
                newUnit = self.createUnit(unitType, unitID, unitPx, unitPy)
                if newUnit:
                    self.allied_units.add(newUnit)
                
        for enemyUnit in rootNode.getElementsByTagName('enemy'):
            for unit in enemyUnit.getElementsByTagName('unit'):
                unitType = unit.getAttribute('type')
                unitID = int(unit.getAttribute('uid'))
                unitPx = int(unit.getAttribute('x'))
                unitPy = int(unit.getAttribute('y'))
                newUnit = self.createUnit(unitType, unitID, unitPx, unitPy)
                if newUnit:
                    self.enemy_units.add(newUnit)


    def createUnit(self, type, id, px, py):
        if type == "fragata":
            return Fragata(id,(px, py),self.unit_images[0:8])
        elif type == "corbeta":
            return Corbeta(id,(px, py),self.unit_images[8:8*2])
        elif type == "misilera":
            return Misilera(id,(px, py),self.unit_images[8*2:8*3])
        elif type == "auxiliar":
            return Auxiliar(id,(px, py),self.unit_images[8*3:8*4])
        elif type == "sub":
            return Submarino(id,(px, py),self.unit_images[8*4:8*5])
        elif type == "guarda":
            return GuardaCosta(id,(px, py),self.unit_images[8*5:8*6])
        elif type == "soberany":
            return Soberany(id,(px, py),self.unit_images[0:8])
        else:
            print "ERROR: Unit type incorrect"
            return None


def main():
    game = Game()
    game.Run()


if __name__ == '__main__':
    import profile
    profile.run('main()')
    
    
    
        
