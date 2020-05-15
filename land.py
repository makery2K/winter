import pygame
from pygame.locals import *
                 
class Land:
    def __init__(self, display, filename, head, size):
        self.move = (0,0)
        self.display = display
        self.size = size
        self.width = size[0]
        self.height = size[1]
        
        with open(filename, 'r') as f:
            self.map = f.readlines()
        
        self.key = self.map.pop(0)[:-1]
        self.pointer = self.key[0]
        
        self.image = {}
        for index, key in enumerate(self.key):
            fileName = head + str(index) + '.png'
            image = pygame.image.load(fileName)
            self.image[key] = image

        self.colMax, self.rowMax = (self.map.pop(0)).split()
        self.colMax = int(self.colMax)
        self.rowMax = int(self.rowMax)
        
        self.tile=[]
        for x in range(self.colMax):
            columnTile=[]
            if x >= len(self.map):
                self.map.append(self.key[0]*self.rowMax)
            for y in range(self.rowMax):
                rect = pygame.Rect((x*size[0], y*size[1]), size)
                key = self.map[x][y]
                columnTile.append([rect, key])
            self.tile.append(columnTile)
        
    def getCellPos(self, pos):
        col = pos[0] // self.size[0]
        row = pos[1] // self.size[1]
        return (col, row)
    
    def draw(self, showPointer = False):
        for x, columne in enumerate(self.tile):
            for y, (rect, key) in enumerate(columne):
                showedRect = rect.move(self.move)
                #key = cell[1]
                if showPointer and self.pointer != '':            
                    if showedRect.collidepoint(pygame.mouse.get_pos()):
                        key = self.pointer
                        if pygame.mouse.get_pressed()[0]:
                            self.tile[x][y][1] = key
                self.display.blit(self.image[key], showedRect)        
                        
    
