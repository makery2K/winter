import pygame

class Background:
    def __init__(self, display, fileName, size=False):
        self.display = display
        self.move = (0,0)
        image = pygame.image.load(fileName)
        if not size:
            size = image.get_size()
        self.image = pygame.transform.scale(image, size) #changing frame of bg

        self.rect = pygame.Rect((0, 0), size) #where to show

    def draw(self):
        startX, startY = self.move
        if startX != 0:
            startX = startX%self.rect.width - self.rect.width
        if startY != 0:
            startY = startY%self.rect.height - self.rect.height
        rectCopy = self.rect.move(startX, startY)
        while(rectCopy.y < self.display.get_height()):
            while(rectCopy.x < self.display.get_width()):
                self.display.blit(self.image, rectCopy)
                rectCopy.x += rectCopy.width
            rectCopy.x = startX
            rectCopy.y += rectCopy.height
