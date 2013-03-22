#!/usr/bin/python

"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2004/04/14 02:38:47 $"
"""

from PythonCard import model

class Palette(model.Background):

    def on_initialize(self, event):
        self.parent = self.getParent()
        self.images = self.parent.images
        self.components.sliderTile.max = len(self.images)-1
        self.on_sliderTile_select(None)
        

    def on_sliderTile_select(self, event):
        comps = self.components
        canvas = comps.tileCanvas
        tile = comps.sliderTile.value
        canvas.drawBitmapScaled(self.images[tile],(0,0),(64,64))
        #canvas.drawBitmap(self.images[tile])
        comps.lblActualTile.text = 'Tile #'+str(tile)
        self.parent.actualTile = tile

    def on_close(self, event):
        pass

if __name__ == '__main__':
    app = model.Application(Palette)
    app.MainLoop()
