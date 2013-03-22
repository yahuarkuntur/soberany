#! usr/bin/python

import utils.engine2d
from utils.engine2d import *

import os

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W,WINDOW_H),16)
    pygame.display.set_caption('Map Editor')
    back = pygame.Surface(screen.get_size(),16)
    back.fill((0,0,0))
    screen.blit(back,(0,0))

    # Load tile sets
    tiles = []
    for x in range(1,5):
        tiles.append(load_image(os.path.join('gfx','tiles','agua','water0'+str(x)+'.png')))
    for x in range(1,33):
        if x < 10:
            tiles.append(load_image(os.path.join('gfx','tiles','water-grass','water-grass0'+str(x)+'.png')))
        else:
            tiles.append(load_image(os.path.join('gfx','tiles','water-grass','water-grass'+str(x)+'.png')))
        
    tiles.append(load_image(os.path.join('gfx','tiles','grass.gif')))
    tiles.append(load_image(os.path.join('gfx','tiles','desert.gif')))
    tiles.append(load_image(os.path.join('gfx','tiles','swamp.gif')))
    tiles.append(load_image(os.path.join('gfx','tiles','hill.gif')))
    tiles.append(load_image(os.path.join('gfx','tiles','rocks.gif')))
    tiles.append(load_image(os.path.join('gfx','tiles','forest.gif')))
    tiles.append(load_image(os.path.join('gfx','tiles','jungle.gif')))

    
    # Create 2DMap
    Map = Engine2D(tiles)
    Map.createRandomMap()

    # Create Minimap
    miniMap = MiniMap(WIDTH,HEIGHT,MINI_MAP_X,MINI_MAP_Y,screen_w,screen_h)
    miniMap.setMiniMap(Map.map.data,tiles,screen)
    miniMap.drawMiniMap(0,0,screen)
    # Options and Info
    font = pygame.font.Font(None,20)
       
    pygame.display.flip()

    offx = 0
    offy = 0
    dirty = 1
    tile_type = 0
    clock = pygame.time.Clock()
    while 1:
        clock.tick(60)
        k = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        MapX = int(mouse_pos[0]/32)*32
        MapY = int(mouse_pos[1]/32)*32

        
        if mouse_button[0] and not miniMap.rect.collidepoint(mouse_pos):
            nx,ny = Map.setTile(offx,offy,mouse_pos,tile_type,screen)
            if nx >=0 and ny >=0:
                miniMap.setTile(nx,ny,tiles[tile_type])
                dirty = 1
        
        
        if k[K_LEFT] or mouse_pos[0] < 2:
            if offx > 0:
                offx -= 1
                dirty = 1
        elif k[K_RIGHT] or mouse_pos[0] > 640-2:
            if offx < WIDTH-screen_w:
                offx += 1
                dirty = 1
        elif k[K_UP] or mouse_pos[1] < 2:
            if offy > 0:
                offy -= 1
                dirty = 1
        elif k[K_DOWN] or mouse_pos[1] > 480-2:
            if offy < HEIGHT-screen_h:
                offy += 1
                dirty = 1

        
        # Update Map
        if dirty:
            Map.drawMap(offx,offy,back)
            screen.blit(back,(0,0))
            dirty = 0
           
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_SPACE:
                    if tile_type < len(tiles)-1:#33:
                        tile_type += 1
                    else:
                        tile_type = 0
                elif event.key == K_RETURN:
                    #Map.saveMap('newmap')
                    Map.saveMap('testmap')
                elif event.key == K_o:
                    #Map.openMap('newmap')
                    Map.openMap('testmap')
##                    Map.drawMap(offx,offy,screen)
                    miniMap.setMiniMap(Map.map.data,tiles,screen)
                    miniMap.drawMiniMap(0,0,screen)
                    dirty = 1
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if miniMap.rect.collidepoint(event.pos):
                        # minimap jump
                        offx,offy = Map.setFocus(miniMap.getMiniMapPos(event.pos))
                        dirty = 1

        screen.blit(tiles[tile_type],(MapX,MapY))
        miniMap.drawMiniMap(offx,offy,screen)
        #screen.blit(tiles[tile_type],(400,450))
        pygame.display.flip()
        screen.blit(back,(MapX,MapY),(MapX,MapY,32,32))      
                        


if __name__ == '__main__': main()
    
        
