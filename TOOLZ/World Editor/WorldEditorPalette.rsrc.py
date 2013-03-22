{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':'Tile Palette',
          'size':(150, 481),

         'components': [

{'type':'StaticText', 
    'name':'lblActualTile', 
    'position':(15, 85), 
    'size':(55, -1), 
    'alignment':'center', 
    'text':'Tile 000', 
    },

{'type':'Slider', 
    'name':'sliderTile', 
    'position':(95, 0), 
    'size':(35, 403), 
    'labels':False, 
    'layout':'vertical', 
    'max':50, 
    'min':0, 
    'tickFrequency':0, 
    'ticks':True, 
    'value':0, 
    },

{'type':'BitmapCanvas', 
    'name':'tileCanvas', 
    'position':(10, 10), 
    'size':(64, 64), 
    'backgroundColor':(255, 255, 255), 
    },

] # end components
} # end background
] # end backgrounds
} }
