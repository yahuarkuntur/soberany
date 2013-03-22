#!/usr/bin/python

"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2004/04/14 02:38:47 $"
"""

from PythonCard import model, dialog, graphic
from wxPython.wx import *

import os, cPickle, wx
from random import randint
from string import splitfields
import WorldEditorPalette

# Window dimension
WINDOW_W = 640
WINDOW_H = 480

# screen dimensions (in tiles)
screen_w = 15#20
screen_h = 15

half_screen_w = screen_w/2
half_screen_h = screen_h/2

tile_size = 32

# map dimensions
##WIDTH = 100
##HEIGHT = 100

class Map:
    def __init__(self,name,w,h):
        self.name = name
        self.width = w
        self.height = h
        self.data = []


class Editor(model.Background):

    def on_initialize(self, event):
        # center App on screen
        xScreen = wxSystemSettings_GetMetric(wxSYS_SCREEN_X) 
        yScreen = wxSystemSettings_GetMetric(wxSYS_SCREEN_Y) 
        xSize, ySize = self.size 
        xPos = (xScreen-xSize)/2 
        yPos = (yScreen-ySize)/2 
        self.position = (xPos,yPos)
        self.paletteWindow = model.childWindow(self, WorldEditorPalette.Palette)
        self.images = []
        self.components.worldMap.autoRefresh = False
        self.map = None
        self.WIDTH = 100
        self.HEIGHT = 100
        self.changedFile = False
        self.offx = 0
        self.offy = 0
        self.actualTile = 0
        self.load_tileset()
        self.newMap()
        self.drawMap()
        self.Show()
        
    def load_tileset(self):
        # Load tile sets
        tiles = []
        for x in range(9):
            if x < 10:
                tiles.append(graphic.Bitmap(os.path.join('tiles','brian','tile00'+str(x)+'.bmp')))
            elif x < 100:
                tiles.append(graphic.Bitmap(os.path.join('tiles','brian','tile0'+str(x)+'.bmp')))
            else:
                tiles.append(graphic.Bitmap(os.path.join('tiles','brian','tile'+str(x)+'.bmp')))
        self.images = tiles            

    def drawMap(self):
        canvas = self.components.worldMap
        for y in range(self.offy,screen_h+self.offy,1):
            for x in range(self.offx,screen_w+self.offx,1):
                canvas.drawBitmap(self.images[self.map.data[x+y*self.WIDTH]], ((x-self.offx)*tile_size,(y-self.offy)*tile_size))
        canvas.refresh()

    def newMap(self):
        self.map = Map('Default Map',self.WIDTH,self.HEIGHT)
        print self.map.name
        print self.map.width
        print self.map.height
        max_tiles = len(self.images)-1
        for y in range(self.map.height):
            for x in range(self.map.width):
                tile = 0#randint(0,max_tiles)
                self.map.data.append(tile)

    def screenToMap(self,pos):
        x,y = pos
        return x/tile_size + self.offx, y/tile_size + self.offy
        
    def saveMap(self, path):
        cPickle.dump(self.map, open(path, "wb"), 1)

    def exportXMLMap(self, path):
        f = open(path, "w")
        f.write(str('<?xml version="1.0" encoding="iso-8859-1"?>')+'\r\n')
        f.write(str('<map name = "new map" width = "'+str(self.WIDTH)+'" height = "'+str(self.HEIGHT)+'">')+'\r\n')
        for data in self.map.data:
            f.write(str('\t<tile type = "'+str(data)+'"/>')+'\r\n')
        f.write(str('</map>'))
        f.close()
    
    def openMap(self, path):
        map = cPickle.load(open(path))
        self.map = map
        self.drawMap()

    def on_cmdSizeOK_mouseClick(self, evt):
        comps = self.components
        save = self.saveChanges()
        if save == "Cancel":
            # don't do anything, just go back to editing
            return
        elif save == "No":
            # any changes will be lost
            pass
        else:
            self.on_cmdSave_mouseClick(event)
        case = comps.mapSize.stringSelection
        print case
        if case == '150x150':
            self.WIDTH = self.HEIGHT = 150
        if case == '100x100':
            self.WIDTH = self.HEIGHT = 100
        if case == '50x50':
            self.WIDTH = self.HEIGHT = 50
        if case == 'custom':
            xxx = comps.txtMapSize.text
            ddd = splitfields(xxx,'x')
            if int(ddd[0]) >= screen_w and int(ddd[1]) >= screen_h:
                self.WIDTH = int(ddd[0])
                self.HEIGHT = int(ddd[1])
            else:
                dialog.alertDialog(self, 'Map size is not supported.','Error')
                return
        comps.sliderX.max = self.WIDTH - screen_w
        comps.sliderY.max = self.HEIGHT - screen_h
        comps.sliderX.value = 0
        comps.sliderY.value = 0
        print 'New dimensions',self.WIDTH, self.HEIGHT
        self.newMap()
        self.drawMap()
        

    def on_sliderX_select(self, event):
        comps = self.components
        #comps.lblMapCoords.text = "Coords : "+str(comps.sliderX.value)+','+str(comps.sliderY.value)
        self.offx = comps.sliderX.value
        self.offy = comps.sliderY.value
        self.drawMap()

    def on_sliderY_select(self, event):
        comps = self.components
        #comps.lblMapCoords.text = "Coords : "+str(comps.sliderX.value)+','+str(comps.sliderY.value)
        self.offx = comps.sliderX.value
        self.offy = comps.sliderY.value
        self.drawMap()
        
    def on_cmdQuit_mouseClick(self, event):
        if self.changedFile:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                return
            elif save == "No":
                # any changes will be lost
                pass
            else:
                self.on_cmdSave_mouseClick(event)
        self.close()

    def on_cmdSave_mouseClick(self, event):
        wildcard = "Map files (*.map)|*.MAP;*.map|All files (*.*)|*.*"
        dir = os.path.dirname('.')
        filename = os.path.basename('NewMap')
        result = dialog.saveFileDialog(None, "Save Map", dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.saveMap(path)
            self.changedFile = False
            return True
        else:
            return False

    def on_cmdExportXML_mouseClick(self, event):
        wildcard = "XML files (*.xml)|*.XML;*.xml|All files (*.*)|*.*"
        dir = os.path.dirname('.')
        filename = os.path.basename('NewMap')
        result = dialog.saveFileDialog(None, "Export XML Map", dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.exportXMLMap(path)
            self.changedFile = False
            return True
        else:
            return False    

    def on_cmdOpen_mouseClick(self, event):
        if self.changedFile:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                return
            elif save == "No":
                # any changes will be lost
                pass
            else:
                self.on_cmdSave_mouseClick(event)
        wildcard = "Map files (*.map)|*.map;*.MAP|All files (*.*)|*.*"
        dir = os.path.dirname('.')
        filename = ""#os.path.basename('NewMap')
        result = dialog.openFileDialog(None, "Open Map", dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.openMap(path)
            self.changedFile = True

    def saveChanges(self):
        msg = "The World Map has changed.\n\nDo you want to save the changes?"
        result = dialog.messageDialog(self, msg, 'World Editor', wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL)
        return result.returnedString


    def on_cmdNew_mouseClick(self, event):
        if self.changedFile:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                return
            elif save == "No":
                # any changes will be lost
                pass
            else:
                self.on_cmdSave_mouseClick(event)
        self.newMap()
        self.drawMap()
        self.changedFile = True

    def on_worldMap_mouseMove(self, event):
        comps = self.components
        x,y = self.screenToMap(event.position)
        self.statusBar.text = '('+str(x)+','+str(y)+')'
        #comps.lblMapCoords.text = "Map Coords : "+str(x)+','+str(y)

    def on_worldMap_mouseDown(self, event):
        comps = self.components
        canvas = self.components.worldMap
        x,y = self.screenToMap(event.position)
        print 'click at',x,y
        self.map.data[x+y*self.WIDTH] = self.actualTile
        canvas.drawBitmap(self.images[self.actualTile], ((x-self.offx)*tile_size,(y-self.offy)*tile_size))
        canvas.refresh()
        self.changedFile = True

    def on_cmdTileset_mouseClick(self, event):
        wildcard = "Image files (*.png)|*.png;*.PNG|All files (*.*)|*.*"
        result = dialog.openFileDialog(None, "Open TileSet", "", "", wildcard)
        if result.accepted:
            # TODO: check if valid!!!
            path = result.paths[0]
            self.loadTileSet(path)


if __name__ == '__main__':
    app = model.Application(Editor)
    app.MainLoop()
