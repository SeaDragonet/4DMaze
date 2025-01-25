import pygame, sys
from pygame.locals import *
import random
from tkinter import *
import tkinter.filedialog, tkinter.messagebox

# Initialize program
Tk().withdraw()
pygame.init()
 
# Assign FPS a value
FPS = 30
FramePerSec = pygame.time.Clock()
 
# Setting up color objects
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
font = pygame.font.Font('arial.ttf', 32)

# Define board cell states. Ana is positive w, kata is negative w
OPEN = 1
PORTALUP = 2
PORTALDOWN = 4
PORTALANA = 8
PORTALKATA = 16
START = 32
VICTORY = 64

# Define directions. Directions are +- x y z w respectively
EAST = 0
WEST = 1
SOUTH = 2
NORTH = 3
UP = 4
DOWN = 5
ANA = 6
KATA = 7

# Define the arrows
ARROWUP = ((16, 14), (25, 5), (34, 14))
ARROWDOWN = ((34, 36), (25, 45), (16, 36))
ARROWANA = ((36, 16), (45, 25), (36, 34))
ARROWKATA = ((14, 34), (5, 25), (14, 16))

# Define grid coords and grid size
GRIDSIZE = 50

IsOverview = False
 
# Setup a 300x300 pixel display with a caption
DISPLAYSURF = pygame.display.set_mode(((GRIDSIZE*10),(GRIDSIZE*10+50)))
DISPLAYSURF.fill(GRAY)
caption = ["It's 4D!", "It's what the cool kids play.", "Help! I am trapped in a 4D maze!", "Hyper Dimensional!", "Press alt f4 to get out of the maze!", "Be glad I made this 10/10/3/3 and not 10/10/10/10.", "Ello there world!", "Your ana or my ana?", "TEMP FIX-REMOVE"]

pygame.display.set_caption(caption[random.randint(0, 8)])
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

# Define the location class
class Location():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0
    def move(self, direction, model, player):
        new = [self.x,self.y,self.z,self.w]
        # Add check to see if 3 and 4d moves are on portals
        match direction:
            case 0:
                new[0] += 1
            case 1:
                new[0] -= 1
            case 2:
                new[1] += 1
            case 3:
                new[1] -= 1
            case 4:
                if player.isEditor():
                    new[2] += 1
                elif model.stateCheck(self.x,self.y,self.z,self.w,PORTALUP):
                    new[2] += 1
            case 5:
                if player.isEditor():
                    new[2] -= 1
                elif model.stateCheck(self.x,self.y,self.z,self.w,PORTALDOWN):
                    new[2] -= 1
            case 6:
                if player.isEditor():
                    new[3] += 1
                elif model.stateCheck(self.x,self.y,self.z,self.w,PORTALANA):
                    new[3] += 1
            case 7:
                if player.isEditor():
                    new[3] -= 1
                elif model.stateCheck(self.x,self.y,self.z,self.w,PORTALKATA):
                    new[3] -= 1
        if not player.isEditor():
            if model.inBounds(new[0],new[1],new[2],new[3]) and model.isOpen(new[0],new[1],new[2],new[3]):
                self.x, self.y, self.z, self.w = new
        elif model.inBounds(new[0],new[1],new[2],new[3]):
                self.x, self.y, self.z, self.w = new
        else:
            pass


# Define the player classs
class Player(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__() 
        self.player = pygame.image.load("Mr eyes.png").convert()
        self.image = pygame.image.load("titled.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.location = location
        self.mode = 0
    def update(self):
        global IsOverview
        if IsOverview:
            pygame.transform.scale()
        else:
            self.rect.centerx = (self.location.x * GRIDSIZE + (0.5 * GRIDSIZE))
            self.rect.centery = (self.location.y * GRIDSIZE + (0.5 * GRIDSIZE))
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def toggleMode(self):
        self.mode ^= 1
    def isEditor(self):
        if self.mode == 1:
            return True
        else:
            return False

# Define the board class
class BoardModel():
    def __init__(self, x=10, y=10, z=3, w=3):
        self.sizex = x
        self.sizey = y
        self.sizez = z
        self.sizew = w
        row = self.sizex*[0]
        self._gameboard = []
        for i in range(self.sizew):
            stack = []
            for j in range(self.sizez):
                layer = []
                for k in range(self.sizey):
                    layer.append(row.copy())
                stack.append(layer.copy())
            self._gameboard.append(stack.copy())
    def isOpen(self, x, y, z, w):
        return self._gameboard[w][z][y][x] >= 1
    def toggleState(self, x, y, z, w, state):
        self._gameboard[w][z][y][x] ^= state
    def inBounds(self, x, y, z, w):
        return 0 <= x < self.sizex and 0 <= y < self.sizey and 0 <= z < self.sizez and 0 <= w < self.sizew
    def stateCheck(self, x, y, z, w, state):
        if self._gameboard[w][z][y][x] & state > 0:
            return True
        else:
            return False
    def getLayer(self,z,w):
        return self._gameboard[w][z]
    def getCell(self, x, y, z, w):
        return self._gameboard[w][z][y][x]
    def setLayer(self, z, w, layer):
        self._gameboard[w][z] = layer


        

class BoardView():
    def __init__(self, model, location):
        self.location = location
        self.model = model
    def drawLayer(self):
        layer = self.model.getLayer(self.location.z, self.location.w)
        for y in range (len(layer)):
            row = layer[y]
            for x in range (len(row)):
                if layer[y][x] == 0:
                    pygame.draw.rect(DISPLAYSURF, BLACK, Rect(x*GRIDSIZE, y*GRIDSIZE, GRIDSIZE, GRIDSIZE))
                else:
                    pygame.draw.rect(DISPLAYSURF, WHITE, Rect(x*GRIDSIZE, y*GRIDSIZE, GRIDSIZE, GRIDSIZE))
                    if layer[y][x] & 2:
                        self.DrawArrow(x*GRIDSIZE, y*GRIDSIZE, 1, RED, ARROWUP)
                    if layer[y][x] & 4:
                        self.DrawArrow(x*GRIDSIZE, y*GRIDSIZE, 1, GREEN, ARROWDOWN)
                    if layer[y][x] & 8:
                        self.DrawArrow(x*GRIDSIZE, y*GRIDSIZE, 1, BLUE, ARROWANA)
                    if layer[y][x] & 16:
                        self.DrawArrow(x*GRIDSIZE, y*GRIDSIZE, 1, PURPLE, ARROWKATA)
    def DrawArrow(self, x, y, scale, color, points):
        pts = []
        for p in points:
            pts.append((p[0]*scale + x, p[1]*scale + y))
        pygame.draw.polygon(DISPLAYSURF, color, pts, 2)

class BoardController():
    def __init__(self,model,location):
        self.model = model
        self.location = location
    def editBoard(self, key):
        if key == K_SPACE: 
            if not self.model.isOpen(self.location.x, self.location.y, self.location.z, self.location.w):
                self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w, OPEN)
        if key == K_UP and self.model.inBounds(self.location.x,self.location.y,self.location.z+1,self.location.w):
            self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w, PORTALUP)
            self.model.toggleState(self.location.x, self.location.y, self.location.z+1, self.location.w, PORTALDOWN)
        if key == K_DOWN and self.model.inBounds(self.location.x,self.location.y,self.location.z-1,self.location.w):
            self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w, PORTALDOWN)
            self.model.toggleState(self.location.x, self.location.y, self.location.z-1, self.location.w, PORTALUP)
        if key == K_RIGHT and self.model.inBounds(self.location.x,self.location.y,self.location.z,self.location.w+1):
            self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w, PORTALANA)
            self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w+1, PORTALKATA)
        if key == K_LEFT and self.model.inBounds(self.location.x,self.location.y,self.location.z,self.location.w-1):
            self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w, PORTALKATA)
            self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w-1, PORTALANA)
        if key == K_q:
            self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w, START)
        if key == K_e:
            self.model.toggleState(self.location.x, self.location.y, self.location.z, self.location.w, VICTORY)

def DrawText(x, y, txt):
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render(txt, True, BLACK, GRAY)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (x, y)

    DISPLAYSURF.blit(text, textRect)

def save(gameboard, file):
    # file = open(name, "w")
    for i in range(gameboard.sizew):
        for j in range(gameboard.sizez):
            for k in range(gameboard.sizey):
                for m in range(gameboard.sizex):
                    print(gameboard.getCell(m, k, j, i), end=" ", file=file)
                file.write("\n")
                # row = board[i][j][k] 
                # print(row, file = file)
            file.write("\n")
    file.close()

def ReadLayer(gameboard, file):
    layer = []
    for k in range(gameboard.sizey):
        line = file.readline()
        items = line.split()
        row = [int(s) for s in items]
        layer.append(row)
    file.readline()   # skip the separator line
    return layer

def LoadBoard(gameboard, file):
    for i in range(gameboard.sizew):
        for j in range(gameboard.sizez):
            gameboard.setLayer(j, i, ReadLayer(gameboard, file))

def main():
    gameLocation = Location()
    gameBoardModel = BoardModel()
    gameBoardController = BoardController(gameBoardModel, gameLocation)
    gameBoardView = BoardView(gameBoardModel, gameLocation)
    gamePlayer = Player(gameLocation)

    gameBoardView.drawLayer()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                    gameLocation.move(WEST, gameBoardModel, gamePlayer)
                if event.key == K_d:
                    gameLocation.move(EAST, gameBoardModel, gamePlayer)
                if event.key == K_w:
                    gameLocation.move(NORTH, gameBoardModel, gamePlayer)
                if event.key == K_s:
                    gameLocation.move(SOUTH, gameBoardModel, gamePlayer)
                if event.key == K_p:
                    file = tkinter.filedialog.asksaveasfile()
                    if file:
                        save(gameBoardModel, file)
                if event.key == K_o:
                    name = tkinter.filedialog.askopenfilename()
                    if name != "":
                        file = open(name)
                        LoadBoard(gameBoardModel, file)  
                if event.key == K_SPACE:
                    gameBoardController.editBoard(K_SPACE)
                if event.key == K_TAB:
                    gamePlayer.toggleMode()
                if event.mod & 3 != 0 and gamePlayer.isEditor():
                    gameBoardController.editBoard(event.key)
                else:
                    if event.key == K_UP:
                        gameLocation.move(UP, gameBoardModel, gamePlayer)
                    if event.key == K_DOWN:
                        gameLocation.move(DOWN, gameBoardModel, gamePlayer)
                    if event.key == K_RIGHT:
                        gameLocation.move(ANA, gameBoardModel, gamePlayer)
                    if event.key == K_LEFT:
                        gameLocation.move(KATA, gameBoardModel, gamePlayer)
        gameBoardView.drawLayer()
        gamePlayer.update()
        gamePlayer.draw(DISPLAYSURF)
        numtext = f"X={gameLocation.x}, Y={gameLocation.y}, Z={gameLocation.z}, W={gameLocation.w}, {gameLocation.x}/{gameLocation.y}/{gameLocation.z}/{gameLocation.w}"
        DrawText((GRIDSIZE*5), (GRIDSIZE*10+25), "ello there world")
        DrawText((GRIDSIZE*5), (GRIDSIZE*10+25), numtext)
        pygame.display.update()
        FramePerSec.tick(FPS)

main()
