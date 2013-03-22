import pygame
from pygame.locals import *

import widget
from widget import  *

import event
from event import  *

import button
from button import Button

import label
from label import Label

import utils
from utils import  *

#===================================================================================
class MenuSweet(ObjetoGUI):
    def __init__(self, botones, label, pos, imagen=None, topspace=50, contenedor=None):
        ObjetoGUI.__init__(self, contenedor)
        self.botones = botones
        self.titulo  = label
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.center = pos
        self.clickeado = 0
        self.visible = True
        self.topspace  = topspace
    #----------------------------------------------------------------------                    
    def actualizar(self, pantalla):
        if not self.visible:
            return
        pantalla.blit(self.imagen, self.rect)

        x = self.rect.left
        w = self.rect.width
        h = self.rect.height

        cuadro = self.imagen.get_rect()
        
        cuadro.left = x + abs(w - self.titulo.getAncho())/2
        cuadro.top  = self.rect.top + self.topspace/2
        self.titulo.mover(cuadro)

        y = self.rect.top + self.titulo.getAlto()
        
        self.titulo.actualizar(pantalla)
        i=1
        for b in self.botones:
            cuadro.left = x + abs(w - b.getAncho())/2
            cuadro.top  = y + (i*b.getAlto() + self.topspace)
            b.mover(cuadro)
            i+=1
            b.actualizar(pantalla)
    #----------------------------------------------------------------------
    def getClicked(self):
        return self.clickeado
    #----------------------------------------------------------------------
    def notificar(self, evento):
        bot_raton    = evento.estMouse()            
        pos_raton    = evento.posMouse()
        i = 1
        for b in self.botones:
            b.notificar(evento)
            if b.estadoClick():
                self.clickeado = i
            i+=1
            
#===================================================================================
#                               FUNCION PRINCIPAL
#===================================================================================
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Ejemplo etiqueta')
    fondo = pygame.Surface(pantalla.get_size())
    fondo.fill((255,255,255))
    pantalla.blit(fondo,(0,0))

    relog = pygame.time.Clock()
    tick_relog = relog.tick

    MiEvento = Evento()
    # La etiqueta
    fondolbl = cargar_imagen('imagenes','fondo_label1.bmp',(255,0,0))
    label = Etiqueta('Hola Diego: Bienvenido',(255,0,0),(300,300),(0,0,0),fondolbl)
    # Los botones
    cmascara = (255,0,0)
    imaB1 = []
    imaB1.append(cargar_imagen('botones','boton1.bmp',cmascara))
    imaB1.append(cargar_imagen('botones','boton2.bmp',cmascara))
    imaB1.append(cargar_imagen('botones','boton3.bmp',cmascara))
    imaB1.append(cargar_imagen('botones','b2_icono1.bmp',cmascara))
    imaB2 = []
    imaB2.append(cargar_imagen('botones','b2_normal.bmp',cmascara))
    imaB2.append(cargar_imagen('botones','b2_selected.bmp',cmascara))
    imaB2.append(cargar_imagen('botones','b2_pressed.bmp',cmascara))
    imaB2.append(cargar_imagen('botones','b2_icono2.bmp',cmascara))
    imaB3 = []
    imaB3.append(cargar_imagen('botones','b2_normal.bmp',cmascara))
    imaB3.append(cargar_imagen('botones','b2_selected.bmp',cmascara))
    imaB3.append(cargar_imagen('botones','b2_pressed.bmp',cmascara))
    imaB3.append(cargar_imagen('botones','b2_icono3.bmp',cmascara))

    imaB4 = []
    imaB4.append(cargar_imagen('botones','b1_normal.bmp',cmascara))
    imaB4.append(cargar_imagen('botones','b1_selected.bmp',cmascara))
    imaB4.append(cargar_imagen('botones','b1_pressed.bmp',cmascara))
    imaB4.append(cargar_imagen('botones','b1_icono1.bmp',cmascara))
    
    boton1 = Boton('cmdBoton1',imaB1,(0,0))
    boton2 = Boton('cmdBoton2',imaB2,(0,0))
    boton3 = Boton('cmdBoton3',imaB3,(0,0))
    boton4 = Boton('cmdBoton4',imaB4,(0,0))        

    botones = []
    botones.append(boton1)
    botones.append(boton2)
    botones.append(boton3)
    botones.append(boton4)    
    
    # El menu
    imagenMenu = cargar_imagen('imagenes','fondo_menu2.bmp')
    menu = MenuSweet(botones,label,(300,300),imagenMenu)

    while 1:
        tick_relog(60)

        menu.notificar(MiEvento)
        
        for evento in pygame.event.get():
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    return
        if menu.getClicked() == 3: return
          
        pantalla.blit(fondo,(0,0))                           
        menu.actualizar(pantalla)
        pygame.display.flip()


#===================================================================================

if __name__ == '__main__': main()
    
