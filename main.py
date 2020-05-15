'''
https://www.gameart2d.com/free-dino-sprites.html

https://www.gameart2d.com/winter-platformer-game-tileset.html
or
https://opengameart.org/content/winter-platformer-game-tileset

https://opengameart.org/content/high-res-fire-ball
'''

import pygame
from pygame.locals import *
from background import *
from land import *

from random import randint

pygame.init()


# pygame.mixer.init()
win = pygame.display.set_mode((128 * 6, 128 * 4))
pygame.display.set_caption("First Game")

x = 0
bg = Background(win, './BG/bg.png') # 
land = Land(win, 'land.txt', './Land/', (128, 128))


class Item(Land):
    def clear(self, charRect):
        for x, columne in enumerate(self.tile):
            for y, (rect, key) in enumerate(columne):
                if rect.colliderect(charRect) and key != self.key[0]:
                    get = self.tile[x][y][1]
                    self.tile[x][y][1] = self.key[0]
                    return get


item = Item(win, 'item.txt', './Item/item', (128, 128))

fireFrame = []
for i in range(1, 7):
    name = './Fire/red' + str(i) + '.png'
    img = pygame.image.load(name)
    fireFrame.append(img)


class Fire:
    def __init__(self):
        self.rect = Rect(x + 1500, randint(char.rect.bottom-200, char.rect.bottom-100), 0, 0)
        self.v = randint(-40, -20)
        self.index = 0
        self.killed = False

    def draw(self):
        self.index += 1
        self.index %= len(fireFrame)
        self.rect.size = fireFrame[self.index].get_size()
        self.rect.x += self.v

        showedRect = self.rect.move(-x, 0)
        self.killed = showedRect.right < 0
        win.blit(fireFrame[self.index], showedRect)


class Character:
    def __init__(self):
        folder = './Character/'
        self.walkFrame = []
        for i in range(1, 11):
            name = folder + 'Walk (' + str(i) + ').png'
            img = pygame.image.load(name)
            self.walkFrame.append(img)

        self.jumpFrame = []
        for i in range(1, 13):
            name = folder + 'Jump (' + str(i) + ').png'
            img = pygame.image.load(name)
            self.jumpFrame.append(img)

        self.idleFrame = []
        for i in range(1, 11):
            name = folder + 'Idle (' + str(i) + ').png'
            img = pygame.image.load(name)
            self.idleFrame.append(img)

        self.runFrame = []
        for i in range(1, 9):
            name = folder + 'Run (' + str(i) + ').png'
            img = pygame.image.load(name)
            self.runFrame.append(img)

        self.deadFrame = []
        for i in range(1, 9):
            name = folder + 'Dead (' + str(i) + ').png'
            img = pygame.image.load(name)
            self.deadFrame.append(img)

        self.rect = pygame.Rect(500, 200, 0, 0)

        self.idxIdleFrm = 0
        self.idxWalkFrm = 0
        self.idxDeadFrm = 0
        self.idxJumpFrm = 0

        self.surface = self.walkFrame[0]
        self.isLeft = False
        self.vy = 0
        self.ay = 0
        self.standing = False

    def walk(self):
        self.idxWalkFrm += 1
        self.idxWalkFrm %= len(self.walkFrame)
        self.surface = self.walkFrame[self.idxWalkFrm]

    def dead(self):
        self.surface = self.deadFrame[self.idxDeadFrm]
  
    def jump(self):
        if self.ay == 0:
            self.vy = -17
            self.idxJumpFrm = 0

        self.surface = self.jumpFrame[self.idxJumpFrm]

        self.idxJumpFrm += 1
        if self.vy < 0 and self.idxJumpFrm > 5:
            self.idxJumpFrm = 5
        elif self.vy > 0 and self.idxJumpFrm > 11:
            self.idxJumpFrm = 11

    def physics(self):
        # 프레임이 전환됐을 때 바닥위치가 바뀌는 것을 방지
        global x, gameState

        bottom = self.rect.bottom
        self.rect.size = self.surface.get_size()
        self.rect.bottom = bottom

        self.rect.centerx = win.get_width()//2 + x
        self.rect.y += int(self.vy)
        self.vy += self.ay

        col, row = land.getCellPos(self.rect.midbottom)
        if land.map[col][row] == land.key[0]:
            self.ay = 1.5
        else:
            self.rect.bottom = land.tile[col][row][0].top
            self.vy = self.ay = 0

        if land.map[col][row] =='B':
            gameState = 'dead'

        if self.isLeft:
            if land.map[col - 1][row - 1] != land.key[0]:
                if self.rect.left < land.tile[col - 1][row - 1][0].right:
                    x -= (self.rect.left - land.tile[col - 1][row - 1][0].right)
        else:
            if land.map[col + 1][row - 1] != land.key[0] and row-1>0:
                if self.rect.right > land.tile[col + 1][row - 1][0].left:
                    x -= (self.rect.right - land.tile[col + 1][row - 1][0].left)

    def draw(self):
        self.physics()
        rectCopy = self.rect.move(-x, 0)
        imageCopy = pygame.transform.flip(self.surface, self.isLeft, False)
        win.blit(imageCopy, rectCopy)

        self.idxIdleFrm += 1
        self.idxIdleFrm %= len(self.idleFrame)
        self.surface = self.idleFrame[self.idxIdleFrm]


char = Character()

clock = pygame.time.Clock()

fireX = 100

fires = []

sysfont = pygame.font.SysFont(None, 200)
lifeNum = 5
lifeMax = 5

life = [pygame.image.load('./Interface/life0.png'), pygame.image.load('./Interface/life1.png')]

gameState = 'running'
while gameState=='running':
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameState = 'dead'

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  # left
        if x>0:
            x -= 10
            char.isLeft = True
            char.walk()

    if keys[pygame.K_RIGHT]:  # right
        if land.colMax*land.width > land.display.get_width()+x:
            x += 10
            char.isLeft = False
            char.walk()

    if keys[pygame.K_UP]:  # up
        char.jump()

    bg.move = int(x * -0.2), 0
    bg.draw()

    land.move = -x, 0
    land.draw()

    item.move = -x, 0
    item.draw()

    get=item.clear(char.rect)
    if get=='1':
        lifeNum +=1
    elif get=='2':
        lifeNum +=0.5
    elif get=='4':
        gameState = 'win'
    
    char.draw()

    if randint(0, 50) == 0:
        fires.append(Fire())

    for i, fire in enumerate(fires):
        fire.draw()
        if fire.rect.colliderect(char.rect):
            del (fires[i])
            lifeNum -= 0.2
        if fire.killed:
            del (fires[i])
            
    lifeNum = round(lifeNum, 1)
    lifeMax = int(max(lifeMax, lifeNum))
    message = sysfont.render(str(lifeNum), True, (100, 100, 100))
    messageRect = message.get_rect()
    win.blit(message, messageRect)
    for i in range(int(lifeNum)):
        win.blit(life[1], (400 + 30*i, 0, 24, 24))
    for i in range(int(lifeNum), lifeMax):
        win.blit(life[0], (400 + 30*i, 0, 24, 24))    
    #pygame.draw.rect(win, (255, 0, 0), (500, 0, point * 10, 10), 0)
    pygame.display.update()

    if lifeNum<0:
        gameState = 'dead'
        
if gameState == 'win':
    rect = Rect(0,0,0,0)
    rect.size = item.image['3'].get_size()
    rect.centerx = win.get_width()//2
    rect.centery = win.get_height()//2
    win.blit(item.image['3'], rect)
    pygame.display.update()
    pygame.time.wait(2000)
    ending = 'You Win'
elif gameState == 'dead':
    for frame in char.deadFrame:
        clock.tick(10)
        bg.draw()
        land.draw()
        item.draw()
        char.surface = frame
        char.draw()
        pygame.display.update()
    ending = 'Gave Over'
message = sysfont.render(ending, True, (100,100,100))
messageRect = message.get_rect()
messageRect.centerx = win.get_width()//2
messageRect.bottom = win.get_height()

for _ in range(80):
    clock.tick(15)
    bg.draw()
    land.draw()
    item.draw()
    char.draw()

    if messageRect.centery >= win.get_height()/2:
        messageRect.y -= 20
    color = [randint(50,150) for _ in range(3)]
    message = sysfont.render(ending, True, color)
    win.blit(message, messageRect)
    pygame.display.update()
pygame.quit()
