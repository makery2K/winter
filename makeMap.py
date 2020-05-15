import pygame
from pygame.locals import *
from background import *
from land import *


pygame.init()
win = pygame.display.set_mode((128*6, 128*4))

x=0
bg = Background(win, './BG/bg.png', (128*12, 128*6))

landFile = 'land.txt'
itemFile = 'item.txt'
land = Land(win, landFile, './Land/', (128,128))

class Item(Land):
    pass
    
item = Item(win, itemFile, './Item/item', (128,128))
pointer = land.key[0]


def append():
    x=len(land.tile)
    columnTile=[]
    for y in range(len(land.tile[-1])):
        rect = pygame.Rect((x*land.width, y*land.height), land.size)
        columnTile.append([rect, 0])
    land.tile.append(columnTile)

    for y in range(len(item.tile[-1])):
        rect = pygame.Rect((x*item.size[0], y*item.size[1]), item.size)
        columnTile.append([rect, 0])
    item.tile.append(columnTile)

def save():
    with open(landFile, 'w') as f:
        f.write(land.key+'\n')
        f.write('{} {}'.format(land.colMax, land.rowMax)+'\n')
        for col in land.tile:
            data = ''.join([key for rect, key in col])
            f.write(data+'\n')

    with open(itemFile, 'w') as f:
        f.write(item.key+'\n')
        f.write('{} {}'.format(item.colMax, item.rowMax)+'\n')
        for col in item.tile:
            data = ''.join([key for rect, key in col])
            f.write(data+'\n')
        
clock = pygame.time.Clock()
runGame = True
while runGame:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            runGame = False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                save()
            elif event.key == K_LEFT:
                x -= land.width if x>0 else 0
            elif event.key == K_RIGHT:
                if land.colMax*land.width > land.display.get_width()+x:
                    x += land.width
                
                   
            else:
                key = event.unicode.upper()
                if key != '':
                    if key in land.key:
                        land.pointer = key
                        item.pointer = ''
                    elif key in item.key:
                        land.pointer = ''
                        item.pointer = key
   
            
      
    bg.move = (int(x*-0.2), 0)
    bg.draw()

    mouseX, mouseY = pygame.mouse.get_pos()
    pointer = (mouseX+x, mouseY)
    land.move = (-x, 0)
    land.draw(True)
    item.move = (-x, 0)
    item.draw(True)

    pygame.display.update() 

pygame.quit()
