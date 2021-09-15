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
GRaY = (128, 128, 128)
font = pygame.font.Font('arial.ttf', 32)


# Define grid coords and grid size
gridx = 0
gridy = 0
gridz = 0
gridw = 0
GRIDSIZE = 50

sizex, sizey, sizez, sizew = (10, 10, 3, 3)

IsOverview = False
 
# Setup a 300x300 pixel display with caption
DISPLAYSURF = pygame.display.set_mode(((GRIDSIZE*10),(GRIDSIZE*10+50)))
DISPLAYSURF.fill(GRaY)

caption = ["It's 4D!", "It's what the cool kids play.", "Help! I am trapped in a 4D maze!", "Hyper Dimensional!", "Press alt f4 to get out of the maze!", "Be glad I made this 10/10/3/3 and not 10/10/10/10.", "Ello there world!", "Not GREY, GRaY!"]

pygame.display.set_caption(caption[random.randint(0, 8)])
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.player = pygame.image.load("Mr eyes.png").convert()
        self.image = pygame.image.load("titled.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        # self.surf = pygame.display.set_mode((600, 600))
        # self.rect = self.surf.get_rect()
 
    def update(self):
        global IsOverview
        if IsOverview:
            pygame.transform.scale()
            
        else:
            self.rect.centerx = (gridx * GRIDSIZE + (0.5 * GRIDSIZE))
            self.rect.centery = (gridy * GRIDSIZE + (0.5 * GRIDSIZE))
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     


mreyes = Player()

def CreateBoard ():
    row = sizex*[0]
    board = []
    for i in range(sizew):
        stack = []
        for j in range(sizez):
            layer = []
            for k in range(sizey):
                layer.append(row.copy())
            stack.append(layer.copy())
        board.append(stack.copy())
    # PrintBoard(board)
    return board

def save(board, file):
    # file = open(name, "w")
    for i in range(sizew):
        for j in range(sizez):
            for k in range(sizey):
                for m in range(sizex):
                    print(board[i][j][k][m], end=" ", file=file)
                file.write("\n")
                # row = board[i][j][k] 
                # print(row, file = file)
            file.write("\n")
    file.close()

def ReadLayer(file):
    layer = []
    for k in range(sizey):
        line = file.readline()
        items = line.split()
        row = [int(s) for s in items]
        layer.append(row)
    file.readline()   # skip the separator line
    return layer

def LoadBoard(board, file):
    for i in range(sizew):
        for j in range(sizez):
            board[i][j] = ReadLayer(file)

def DrawLayer(board, z, w):
    layer = board[w][z]
    for y in range (len(layer)):
        row = layer[y]
        for x in range (len(row)):
            if layer[y][x] == 0:
                pygame.draw.rect(DISPLAYSURF, BLACK, Rect(x*GRIDSIZE, y*GRIDSIZE, GRIDSIZE, GRIDSIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, WHITE, Rect(x*GRIDSIZE, y*GRIDSIZE, GRIDSIZE, GRIDSIZE))
                if layer[y][x] & 2:
                    pygame.draw.polygon(DISPLAYSURF, RED, ((x*GRIDSIZE+16, y*GRIDSIZE+14), (x*GRIDSIZE+25, y*GRIDSIZE+5), (x*GRIDSIZE+34, y*GRIDSIZE+14)), 2)
                if layer[y][x] & 4:
                    pygame.draw.polygon(DISPLAYSURF, GREEN, ((x*GRIDSIZE+34, y*GRIDSIZE+36), (x*GRIDSIZE+25, y*GRIDSIZE+45), (x*GRIDSIZE+16, y*GRIDSIZE+36)), 2)
                if layer[y][x] & 8:
                    pygame.draw.polygon(DISPLAYSURF, BLUE, ((x*GRIDSIZE+36, y*GRIDSIZE+16), (x*GRIDSIZE+45, y*GRIDSIZE+25), (x*GRIDSIZE+36, y*GRIDSIZE+34)), 2)
                if layer[y][x] & 16:
                    pygame.draw.polygon(DISPLAYSURF, PURPLE, ((x*GRIDSIZE+14, y*GRIDSIZE+34), (x*GRIDSIZE+5, y*GRIDSIZE+25), (x*GRIDSIZE+14, y*GRIDSIZE+16)), 2)

    
def DrawText(x, y, txt):
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render(txt, True, BLACK, GRaY)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (x, y)

    DISPLAYSURF.blit(text, textRect)


def PrintBoard(board):
    for row in board:
        print(row)
    print()

def main():
    global gridx, gridy, gridz, gridw
    board = CreateBoard()
    DrawLayer(board, 0, 0)
    # Beginning Game Loop
    while True:     
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a and gridx - 1 > -1:
                    gridx -= 1
                if event.key == K_d and gridx + 1 < sizex:
                    gridx += 1
                if event.key == K_w and gridy - 1 > -1:
                    gridy -= 1
                if event.key == K_s and gridy + 1 < sizey:
                    gridy += 1
                if event.key == K_p:
                    file = tkinter.filedialog.asksaveasfile()
                    if file:
                        save(board, file)
                if event.key == K_o:
                    name = tkinter.filedialog.askopenfilename()
                    if name != "":
                        file = open(name)
                        LoadBoard(board, file)  
                if event.key == K_v:
                    Overview(board, 0)                 
                if event.mod & 3 == 0:
                    if event.key == K_LEFT and gridw - 1 > -1:
                        gridw -= 1
                    if event.key == K_RIGHT and gridw + 1 < sizew:
                        gridw += 1
                    if event.key == K_UP and gridz - 1 > -1:
                        gridz -= 1
                    if event.key == K_DOWN and gridz + 1 < sizez:
                        gridz += 1                
                if event.key == K_SPACE: 
                    if board[gridw][gridz][gridy][gridx]>1:
                        pass
                    else:
                        board[gridw][gridz][gridy][gridx] = (board[gridw][gridz][gridy][gridx]^1) 
                if event.mod & 3 != 0:
                # if 1 == 1:
                    if event.key == K_UP and gridz > 0:
                        board[gridw][gridz][gridy][gridx] = ((board[gridw][gridz][gridy][gridx])^2)
                        board[gridw][gridz-1][gridy][gridx] = ((board[gridw][gridz-1][gridy][gridx])^4)
                    if event.key == K_DOWN and gridz + 1 < sizez:
                        board[gridw][gridz][gridy][gridx] = ((board[gridw][gridz][gridy][gridx])^4)
                        board[gridw][gridz+1][gridy][gridx] = ((board[gridw][gridz+1][gridy][gridx])^2)
                    if event.key == K_RIGHT and gridw + 1 < sizew:
                        board[gridw][gridz][gridy][gridx] = ((board[gridw][gridz][gridy][gridx])^8)
                        board[gridw+1][gridz][gridy][gridx] = ((board[gridw+1][gridz][gridy][gridx])^16)
                    if event.key == K_LEFT and gridw > 0:
                        board[gridw][gridz][gridy][gridx] = ((board[gridw][gridz][gridy][gridx])^16)
                        board[gridw-1][gridz][gridy][gridx] = ((board[gridw-1][gridz][gridy][gridx])^8)
                    if event.key == K_q:
                        board[gridw][gridz][gridy][gridx] = ((board[gridw][gridz][gridy][gridx])^32)
                    if event.key == K_e:
                        board[gridw][gridz][gridy][gridx] = ((board[gridw][gridz][gridy][gridx])^64)
                mreyes.update()
                mreyes.draw(DISPLAYSURF)
                # PrintBoard(board)
                DrawLayer(board, gridz, gridw)
                numtext = f"X={gridx}, Y={gridy}, Z={gridz}, W={gridw}, {gridx}/{gridy}/{gridz}/{gridw}"
                DrawText((GRIDSIZE*5), (GRIDSIZE*10+25), "ello there world")
                DrawText((GRIDSIZE*5), (GRIDSIZE*10+25), numtext)
        
        mreyes.draw(DISPLAYSURF)
            
        pygame.display.update()
        FramePerSec.tick(FPS)

# arrow graphics for d3, d4
aup =   ((16, 14), (25, 5), (34, 14))
adown = ((34, 36), (25, 45), (16, 36))
aright =((36, 16), (45, 25), (36, 34))
aleft = ((14, 34), (5, 25), (14, 16))

def DrawArrow(x, y, scale, color, points):
    pts = []
    for p in points:
        pts.append((p[0]*scale + x, p[1]*scale + y))
    pygame.draw.polygon(DISPLAYSURF, color, pts, 2)


def DrawLayer2(board, z, w, px, py, scale):
    layer = board[w][z]
    size = GRIDSIZE * scale
    for y in range (len(layer)):
        row = layer[y]
        for x in range (len(row)):
            if layer[y][x] == 0:
                pygame.draw.rect(DISPLAYSURF, BLACK, Rect(px + size*x, py + size*y, size, size))
            else:
                pygame.draw.rect(DISPLAYSURF, WHITE, Rect(px + size*x, py + size*y, size, size))
                if layer[y][x] & 2:
                    DrawArrow(px + size*x, py + size*y, scale, RED, aup)
                    #pygame.draw.polygon(DISPLAYSURF, RED, ((x*GRIDSIZE+16, y*GRIDSIZE+14), (x*GRIDSIZE+25, y*GRIDSIZE+5), (x*GRIDSIZE+34, y*GRIDSIZE+14)), 2)
                if layer[y][x] & 4:
                    DrawArrow(px + size*x, py + size*y, scale, GREEN, adown)
                if layer[y][x] & 8:
                    DrawArrow(px + size*x, py + size*y, scale, BLUE, aright)
                if layer[y][x] & 16:
                    DrawArrow(px + size*x, py + size*y, scale, PURPLE, aleft)


def Overview(board, screensize):
    scale = .3
    DISPLAYSURF.fill(GRaY)
    for i in range(sizew):
        px = i * GRIDSIZE * scale * (sizex+1)
        for j in range(sizez):
            py = j * GRIDSIZE * scale * (sizey+1)
            DrawLayer2(board, j, i, px, py, scale)
    while True:
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return        
        pygame.display.update()
        FramePerSec.tick(FPS)


main()
