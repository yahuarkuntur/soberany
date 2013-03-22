# This is an example setup.py file
# run it from the windows command line like so:
# > C:\Python2.4\python.exe setup.py py2exe
 
from distutils.core import setup
 
import py2exe, shutil, os

project_name = 'Soberany'
# extra files/dirs copied to game
extra_data = ['fonts','gfx','maps','misions','sfx'] 

opts = { 
 "py2exe": { 
   # if you import .py files from subfolders of your project, then those are
   # submodules.  You'll want to declare those in the "includes"
   'includes':['utils',
               'utils.all_units',
               'utils.astar',
               'utils.basicunit',
               'utils.common',
               'utils.engine2d',
               'utils.explosion',
               'utils.lifebar',
               'utils.map',
               'utils.message',
               'utils.mision',
               'utils.selbox',
               'utils.selectedunit',
               'utils.settings',
               'utils.sounds',
               'utils.sprite',
               'utils.target',
               'utils.textscroller',
               'utils.unit',
               'utils.wireframe'
               ]
 } 
} 
 
setup(

    version = "0.1",
    description = "Soberany -  A Free & Simple RTS Game",
    name = "Soberany",
 
  #this is the file that is run when you start the game from the command line.  
##  windows=['soberany.py'],
  windows=[{"script": "soberany.py","icon_resources": [(1, "pycon.ico")]}],
 
  #options as defined above
  options=opts,
 
  #data files - these are the non-python files, like images and sounds
  #the glob module comes in handy here.
  #data_files = [],
 
  #this will pack up a zipfile instead of having a glut of files sitting
  #in a folder.
  zipfile="lib/shared.zip"
)


#also need to hand copy the extra files here
def installfile(name):
    dst = os.path.join('dist')
    print 'copying', name, '->', dst
    if os.path.isdir(name):
        dst = os.path.join(dst, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
    else:
        print 'Warning, %s not found' % name

for data in extra_data:
    installfile(data)
