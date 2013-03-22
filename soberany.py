#! usr/bin/python

print 'This is free software, and you are welcome to redistribute it'
print 'under certain conditions; see LICENSE.txt for details.'

print 'Soberany'
print 
import sys, platform
print '*'*80
print 'Platform:',platform.platform()
print 'System:',platform.system()
print 'Python:',sys.version
print '*'*80
print
print 'Importing modules',

import xml.dom
from xml.dom import minidom

import utils.engine2d
from utils.engine2d             import isAlpha, load_image, Engine2D, MiniMap, Point, pp_collide, loadTiles
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
print '\t[DONE]'
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
        # dir = os.path.join('gfx','tiles')
        self.tiles = []
        self.tiles = loadTiles(os.path.join('gfx','tiles','tileset.png'))
    #---------------------------------------------------------------------------------------------------
    def loadMaps(self):
        #self.Engine2D.createMap(0)
        #self.Engine2D.openMap(os.path.join('maps','campains','mision01.xml'))
        self.Engine2D.openMap('testmap')
        # Create Minimap  
        self.miniMap = MiniMap(WIDTH,HEIGHT,MINI_MAP_X,MINI_MAP_Y,screen_w,screen_h)
        self.miniMap.setMiniMap(self.Engine2D.map.data,self.tiles,self.screen)
        self.miniMap.drawMiniMap(0,0,self.screen)
    #---------------------------------------------------------------------------------------------------
    def loadTargetImages(self):
        # dir = os.path.join('gfx','gui')
        self.target_images = []
        for x in range(5):
            self.target_images.append(load_image(os.path.join('gfx','gui','target0'+str(x)+'.gif')))
            
    def loadUnitImages(self):
        # load unit images
        self.unit_images = []
        # fragata
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','fragata','fragata0'+str(x)+'.gif')))
        # corbeta
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','corbeta','corbeta0'+str(x)+'.png'),-1))
        # misilera
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','misilera','misilera0'+str(x)+'.png'),-1))
        # auxiliar
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','auxi','auxi0'+str(x)+'.gif')))
        # guardacosta
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','guarda','guarda0'+str(x)+'.gif')))
        # submarino
        for x in range(1,9):
            self.unit_images.append(load_image(os.path.join('gfx','unit','sub','sub0'+str(x)+'.png'),-1))

    def loadExtras(self):
        # load panel
        self.panel = load_image(os.path.join('gfx','gui','panel.gif'))
        self.panel_rect = self.panel.get_rect()
        self.panel_rect.centerx = 320
        self.panel_rect.bottom = 480

        # create miniunits
        self.allied_mini_unit_surf = pygame.Surface((2,2),16)
        self.allied_mini_unit_surf.fill(ALLIED_UNIT_COLOR)
        self.allied_mini_unit_surf.convert()

        self.enemy_mini_unit_surf = pygame.Surface((2,2),16)
        self.enemy_mini_unit_surf.fill(ENEMY_UNIT_COLOR)
        self.enemy_mini_unit_surf.convert()
        
        # selected unit            
        self.selected = load_image(os.path.join('gfx','unit','extras','selected.gif'))
        # selected enemy
        self.selected2 = load_image(os.path.join('gfx','unit','extras','selected_enemy.gif'))
        # explosions        
        self.explosion_images = []
        for x in range(1,5):
            self.explosion_images.append(load_image(os.path.join('gfx','unit','extras','explosion0'+str(x)+'.gif')))
        # shots
        self.shot_images = []
        for x in range(1,4):
            self.shot_images.append(load_image(os.path.join('gfx','unit','extras','hit0'+str(x)+'.gif')))

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

    def findPath(self,unit,dest):
        start = Point(unit.pos[0],unit.pos[1])
        #start = self.Engine2D.getExpandedPoint(Point(unit.pos[0],unit.pos[1]))
        pathfinder = PathFinder(self.Engine2D.map.data,unit,start,dest)
        print 'iniciando Pathfinder...'
        pathfinder.start()
        unit.setState(WALK)

    def groupWalk(self, dest):
        ### TODO: Coordinated Movement
        # Group movement
        if self.selected_units == []:
            return
        refPoint = Point(self.selected_units[0].pos[0], self.selected_units[0].pos[1])
        for unit in self.selected_units:
            dx = refPoint.x - unit.pos[0]
            dy = refPoint.y - unit.pos[1]
            if dest.x + dx <= WIDTH and dest.y + dy <= HEIGHT:
                # is valid coord???
                newPoint = Point(dest.x + dx, dest.y + dy)
            else:
                newPoint = Point(dest.x, dest.y)
            newdest = self.Engine2D.getExpandedPoint(newPoint)
            unit.target = None
            if newdest != None:
                self.findPath(unit,newdest)
            else:
                print 'ERROR: Invalid destination'

##    def groupWalk(self, dest):
##        ### TODO: Coordinated Movement
##        # Group movement
##        if self.selected_units == []:
##            return
##        x = 0
##        y = 0
##        # max grid is 3x3
##        for unit in self.selected_units:
##            unit.target = None
##            self.findPath(unit,Point(dest.x + x, dest.y + y))
##            if self.Engine2D.isWalkable((dest.x + x, dest.y + y)):
##                self.findPath(unit,Point(dest.x + x, dest.y + y))
##            else:
##                if dest.x + x < WIDTH and x <= 2:
##                    x += 2
##                else:
##                    x = 0
##                    if dest.y + y < HEIGHT and y <= 2:
##                        y += 2
##                    else:
##                        y = 0
##                self.findPath(unit,self.Engine2D.getExpandedPoint(Point(dest.x + x, dest.y + y)))
            
            
            
    def groupUnits(self, num):
        if self.selected_units == []:
            return
        for unit in self.selected_units:
            unit.group = num            

    def callGroup(self, num):
        self.selected_units = []
        for unit in self.allied_units.sprites():
            if unit.group == num:
                self.selected_units.append(unit)
                #self.sound.play(self.fragata_sounds[3])
                self.selected_mark.add(SelectedUnit(self.selected,unit))
                self.life_bars.add(LifeBar(unit))

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
                        self.messages.add('Group 1 assigned')
                        self.groupUnits(1)
                    else:
                        self.callGroup(1)
                elif event.key == K_2:
                    if self.do_group:
                        self.messages.add('Group 2 assigned')
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
                            # enemy unit selected to attack
                            # Group Attack
                            for u in self.selected_units:
                                u.target = unit
                            if u.canAttack():
                                u.setState(ATTACK)
                            else:
                                self.messages.add("Error: Enemy %s cant be attacked." % unit.type)
                                u.target = None
                            return 1

                    if self.miniMap.rect.collidepoint(event.pos):
                        # minimap jump
                        x,y = self.miniMap.getMiniMapPos(event.pos)
                        dest = self.Engine2D.mapToScreen(x-self.offx,y-self.offy)
                        if not self.Engine2D.isWalkable((x,y)):
                            self.messages.add('Invalid coords at: '+str(x)+','+str(y))
                            return 1
                        self.messages.add('Coordinates confirmed at: '+str(x)+','+str(y))
                        ### TODO: Coordinated Movement
                        # Group movement
                        for unit in self.selected_units:
                            self.findPath(unit,Point(x,y))
                            unit.target = None
                        if not self.target:
                            self.target.add(Target(self.target_images,dest))
                    if (self.panel_rect.collidepoint(event.pos) and isAlpha(self.panel,self.panel_rect,event.pos)) or not self.panel_rect.collidepoint(event.pos):
                        # transparent part of panel so we can move
                        x,y = self.Engine2D.screenToMap(event.pos)
                        dest = self.Engine2D.mapToScreen(x-self.offx,y-self.offy)
                        if not self.Engine2D.isWalkable((x,y)):
                            self.messages.add('Invalid coords at: '+str(x)+','+str(y))
                            return 1
                        self.messages.add('Coordinates confirmed at: '+str(x)+','+str(y))
                        ### TODO: Coordinated Movement
                        # Group movement
                        self.groupWalk(Point(x,y))
##                        for unit in self.selected_units:
##                            self.findPath(unit,Point(x,y))
##                            unit.target = None
                        if not self.target:
                            self.target.add(Target(self.target_images,dest))
            elif event.type == MOUSEBUTTONUP:
                # MOUSE BUTTON RELEASED HANDLING
                selection_rect = self.SelBox.getRect()
                if selection_rect:
                    # check selected units
                    for unit in self.allied_units.sprites():
                        if pp_collide(selection_rect,unit):
                            print 'Unit selected'
                            self.selected_units.append(unit)
                            self.sound.play(self.fragata_sounds[3])
                            self.selected_mark.add(SelectedUnit(self.selected,unit))
                            self.life_bars.add(LifeBar(unit))
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

    def showGroupInfo(self):
        units = [0,0,0,0,0,0,0]
        tags = ['Fragatas','Corbetas','Misileras','Auxiliares','Submarinos','Guardacostas','Aeronaves']
        for unit in self.selected_units:
            if unit.type == FRAG and unit.armor > 0:
                units[0] += 1
            elif unit.type == CORB and unit.armor > 0:
                units[1] += 1
            elif unit.type == MISI and unit.armor > 0:
                units[2] += 1
            elif unit.type == AUXI and unit.armor > 0:
                units[3] += 1
            elif unit.type == SUBM and unit.armor > 0:
                units[4] += 1
            elif unit.type == GUAR and unit.armor > 0:
                units[5] += 1
            elif unit.type == AERO and unit.armor > 0:
                units[6] += 1
        cont = 0
        for x in range(len(units)):
            if units[x]:
                surf = self.font.render('('+str(units[x])+') '+tags[x],1,UNIT_INFO_COLOR)
                rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+12*cont)
                self.screen.blit(surf,rect)
                cont += 1
        

    def showUnitInfo(self,unit):
        if unit.armor <= 0:
            return
        # unit type
        surf = self.font.render(str(unit.type).upper(),1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y)
        self.screen.blit(surf,rect)
        # unit rank
        surf = self.font.render(''+unit.rank,1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+12)
        self.screen.blit(surf,rect)
        # unit armor
        surf = self.font.render('Armor: '+str(unit.armor)+'/'+str(unit.armor2),1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+24)
        self.screen.blit(surf,rect)
        # unit damage
        surf = self.font.render('Damage: '+str(unit.damage),1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+36)
        self.screen.blit(surf,rect)
        # unit air damage
        surf = self.font.render('Air damage: '+str(unit.air_damage),1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+48)
        self.screen.blit(surf,rect)
        # fsm info
        surf = self.font.render('AI state: '+FSM_STATES[unit.state],1,UNIT_INFO_COLOR)
        rect = surf.get_rect().move(UNIT_INFO_X,UNIT_INFO_Y+60)
        self.screen.blit(surf,rect)
        

    def clearSprites(self):
        self.screen.blit(self.back,self.fps_rect,self.fps_rect)
        self.target.clear(self.screen, self.back)
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
        self.allied_units.update(ticks, self.offx, self.offy,self.enemy_units.sprites())
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
                    print 'FLEE destination error:', x, y
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
                self.messages.add("Allied %s destroyed." % mu.type)
            else:
                self.miniMap.drawMiniUnit(mu.pos[0],mu.pos[1],self.allied_mini_unit_surf,self.screen)
        for mu in self.enemy_units.sprites():
            if mu.flee_dest != (-1,-1):
                # flee
                x,y = mu.flee_dest
                if self.Engine2D.isWalkable((x,y)):
                    print 'FLEE destination error:', x, y
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
                self.messages.add("Enemy %s destroyed." % mu.type)
            else:
                self.miniMap.drawMiniUnit(mu.pos[0],mu.pos[1],self.enemy_mini_unit_surf,self.screen)


        # blit some info 
        surf = self.font.render('fps = '+str(int(self.clock.get_fps())),1,UNIT_INFO_COLOR)
        self.fps_rect = surf.get_rect().move(5,5)
        self.screen.blit(surf,self.fps_rect)

        # show messages
        self.messages.update(ticks)
        self.messages.draw()

        # show unit info
        if len(self.selected_units) == 1:
            self.showUnitInfo(self.selected_units[0])
        if len(self.selected_units) > 1:
            self.showGroupInfo()
        if self.selected_enemy != None:
            self.showUnitInfo(self.selected_enemy)

        
        
    #................................................................................................        
    def setup(self):
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
        self.font = pygame.font.Font(os.path.join('fonts','vera.ttf'),10)

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

        # create messages
        self.messages = Message(self.font,(10,50),(0,255,0),self.screen,self.back)

        self.dirty = True

        # groups
        self.do_group = False
        # many units can belong to many groups
        self.Group1 = []
        self.Group2 = []


    def main_loop(self):

        mision_back = load_image(os.path.join('gfx','gui','back.png'))
        title_font = pygame.font.Font(os.path.join('fonts','sten.ttf'),50)
        mision_font = pygame.font.Font(os.path.join('fonts','vera.ttf'),14)
        subt_font = pygame.font.Font(os.path.join('fonts','sten.ttf'),20)
        surf = title_font.render('SOBERANY',1,(255,255,255))
        rect = surf.get_rect()
        rect.center = 320,100
        mision_back.blit(surf,rect)
        mision = MisionObjectives(os.path.join('misions','intro.txt'),self.screen,mision_back,mision_font)
        mision.ShowMision()
        surf = subt_font.render('MISSION OBJECTIVES',1,(0,255,0))
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

        title_font = pygame.font.Font(os.path.join('fonts','sten.ttf'),50)
        if not len(self.allied_units):
            pygame.time.wait(1000)
            surf = title_font.render('MISSION FAILED!',1,(255,0,0))
        elif not len(self.enemy_units):
            pygame.time.wait(1000)
            surf = title_font.render('MISSION ACCOMPLISHED!',1,(0,255,0))
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
        print 'Mission name:', misionName

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
        elif type == "guarda":
            return GuardaCosta(id,(px, py),self.unit_images[8*4:8*5])
        elif type == "sub":
            return Submarino(id,(px, py),self.unit_images[8*5:8*6])
        elif type == "soberany":
            return Soberany(id,(px, py),self.unit_images[0:8])
        else:
            print "ERROR: Wrong unit type"
            return None



if __name__ == '__main__':
    game = Game()
    game.Run()
    
    
        
