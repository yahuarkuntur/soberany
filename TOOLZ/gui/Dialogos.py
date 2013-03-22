import pygame
from pygame.locals import *

import event
from event import *

import widget
from widget import *

import utils
from utils import *

import os

class MsgBox(Widget):
    #----------------------------------------------------------------------            
    def __init__(self, mensaje, pos, contenedor=None):
        Widget.__init__(self, contenedor)
        self.crearBoton()
        self.crearMensaje(mensaje)
        # Cargamos la imagen del fondo
        self.imagen = cargar_imagen('imagenes','fondo_msgbox1.bmp',(255,0,0))
        # Creamos el rect y lo posicionamos
        self.rect = self.imagen.get_rect()
        self.rect.center = pos
        self.visible = False
        self.cambios = False
    #----------------------------------------------------------------------
    def crearMensaje(self, mensaje):
        # Creamos la etiqueta donde se coloque el mensaje
        self.eMensaje  = Etiqueta(mensaje,(255,255,0),(300,300),(0,0,0))
    #----------------------------------------------------------------------        
    def crearBoton(self):
        cmascara = (255,0,0)
         # Creamos el boton
        imaBA = []
        imaBA.append(cargar_imagen('botones','b2_normal.bmp',cmascara))
        imaBA.append(cargar_imagen('botones','b2_selected.bmp',cmascara))
        imaBA.append(cargar_imagen('botones','b2_pressed.bmp',cmascara))
        imaBA.append(cargar_imagen('botones','b2_icono4.bmp',cmascara))
        self.bAceptar = Boton('cmdAceptar',imaBA,(0,0))
    #----------------------------------------------------------------------
    def setVisible(self, visible):
        self.visible = visible
        self.cambios = True
    #----------------------------------------------------------------------
    def actualizar(self, pantalla):
        if not self.visible or not self.cambios:
            return
        # La imagen de fondo
        pantalla.blit(self.imagen, self.rect)

        x = self.rect.left
        y = self.rect.top + self.eMensaje.getAlto()
        w = self.rect.width
        h = self.rect.height
        # Dibujando el titulo
        cuadro = self.imagen.get_rect()
        cuadro.left = x + abs(w - self.eMensaje.getAncho())/2
        cuadro.top  = y + 10
        self.eMensaje.mover(cuadro)

        self.eMensaje.actualizar(pantalla)
        # Dibujando el boton
        cuadro.left = x + abs(w - self.bAceptar.getAncho())/2
        cuadro.top  = y + self.bAceptar.getAlto()*2 
        self.bAceptar.mover(cuadro)
        self.bAceptar.actualizar(pantalla)
    #----------------------------------------------------------------------
    def notificar(self, evento):
        if not self.visible:  # No notifica si no esta visible
            return
        bot_raton    = evento.estMouse()            
        pos_raton    = evento.posMouse()
        self.bAceptar.notificar(evento)
        if self.bAceptar.estadoClick():
           self.visible = False
           self.cambios = True
           return True
        return False
#===================================================================================
#                               FUNCION PRINCIPAL
#===================================================================================
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800,600),16)
    pygame.display.set_caption('Ejemplo etiqueta')
    fondo = pygame.Surface(pantalla.get_size(),16)
    fondo.fill((255,255,255))
    pantalla.blit(fondo,(0,0))

    relog = pygame.time.Clock()
    tick_relog = relog.tick

    MiEvento = Event()
    lblAdvertencia  = Etiqueta('Pulse ESC para mostrar el cuadro de dialogo Salir',(0,0,255),(300,100),(0,0,0))
    msgbox = MsgBox('De verdad quiere salir?',(400,300))
    
    r = 0
    g = 0
    b = 0
    ParaSalir = False
    while 1:
        tick_relog(60)
    
        for evento in pygame.event.get():
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    msgbox.setVisible(True)
                    ParaSalir = True
        # Verificar si se hace click
        if ParaSalir:
            if msgbox.notificar(MiEvento):
                return  

        pantalla.blit(fondo,(0,0))
        lblAdvertencia.actualizar(pantalla)
        msgbox.actualizar(pantalla)
        pygame.display.flip()


#===================================================================================

if __name__ == '__main__':
    main()
    
        


    
