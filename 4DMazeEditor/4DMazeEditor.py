import pygame, sys, os
from pygame.locals import *
import operator
from random import randint, randrange
from tkinter import *
import tkinter.filedialog, tkinter.messagebox

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize program
Tk().withdraw()
pygame.init()

# Assign FPS a value
FPS = 30
FramePerSec = pygame.time.Clock()

# Setting up color objects
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRaY = (128, 128, 128)
font = pygame.font.Font("arial.ttf", 32)


# Define grid coords and grid size
gridx = 0
gridy = 0
gridz = 0
gridw = 0
GRIDSIZE = 50

#sizex, sizey, sizez, sizew = (10, 10, 3, 3)
sizex, sizey, sizez, sizew = (7, 7, 4, 4)

def SetupWindow(wx, wy):
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(wx) + "," + str(wy)    

# Setup a 300x300 pixel display with caption
SetupWindow(0, 30)
DISPLAYSURF = pygame.display.set_mode(((GRIDSIZE * 10), (GRIDSIZE * 10 + 50)))
DISPLAYSURF.fill(GRaY)
pygame.display.set_caption("It's 4D!")
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
        self.rect.centerx = int(gridx * GRIDSIZE + (0.5 * GRIDSIZE))
        self.rect.centery = int(gridy * GRIDSIZE + (0.5 * GRIDSIZE))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


mreyes = Player()


def CreateBoard():
    row = sizex * [0]
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
    file.readline()  # skip the separator line
    return layer


def LoadBoard(board, file):
    for i in range(sizew):
        for j in range(sizez):
            board[i][j] = ReadLayer(file)


def DrawLayer(board, z, w):
    layer = board[w][z]
    for y in range(len(layer)):
        row = layer[y]
        for x in range(len(row)):
            if layer[y][x] == 0:
                pygame.draw.rect(
                    DISPLAYSURF,
                    BLACK,
                    Rect(x * GRIDSIZE, y * GRIDSIZE, GRIDSIZE, GRIDSIZE),
                )
            else:
                pygame.draw.rect(
                    DISPLAYSURF,
                    WHITE,
                    Rect(x * GRIDSIZE, y * GRIDSIZE, GRIDSIZE, GRIDSIZE),
                )
                if layer[y][x] & 2:
                    pygame.draw.polygon(
                        DISPLAYSURF,
                        RED,
                        (
                            (x * GRIDSIZE + 16, y * GRIDSIZE + 14),
                            (x * GRIDSIZE + 25, y * GRIDSIZE + 5),
                            (x * GRIDSIZE + 34, y * GRIDSIZE + 14),
                        ),
                        2,
                    )
                if layer[y][x] & 4:
                    pygame.draw.polygon(
                        DISPLAYSURF,
                        GREEN,
                        (
                            (x * GRIDSIZE + 34, y * GRIDSIZE + 36),
                            (x * GRIDSIZE + 25, y * GRIDSIZE + 45),
                            (x * GRIDSIZE + 16, y * GRIDSIZE + 36),
                        ),
                        2,
                    )
                if layer[y][x] & 8:
                    pygame.draw.polygon(
                        DISPLAYSURF,
                        BLUE,
                        (
                            (x * GRIDSIZE + 36, y * GRIDSIZE + 16),
                            (x * GRIDSIZE + 45, y * GRIDSIZE + 25),
                            (x * GRIDSIZE + 36, y * GRIDSIZE + 34),
                        ),
                        2,
                    )
                if layer[y][x] & 16:
                    pygame.draw.polygon(
                        DISPLAYSURF,
                        PURPLE,
                        (
                            (x * GRIDSIZE + 14, y * GRIDSIZE + 34),
                            (x * GRIDSIZE + 5, y * GRIDSIZE + 25),
                            (x * GRIDSIZE + 14, y * GRIDSIZE + 16),
                        ),
                        2,
                    )


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
                    Overview(board)
                if event.key == K_t:
                    TunnelWorm(board, 40)
                    Overview(board)
                if event.mod == 0:
                    if event.key == K_LEFT and gridw - 1 > -1:
                        gridw -= 1
                    if event.key == K_RIGHT and gridw + 1 < sizew:
                        gridw += 1
                    if event.key == K_UP and gridz - 1 > -1:
                        gridz -= 1
                    if event.key == K_DOWN and gridz + 1 < sizez:
                        gridz += 1
                if event.key == K_SPACE:
                    if board[gridw][gridz][gridy][gridx] > 1:
                        if event.mod & 3:  # shift key force-clears a space
                            board[gridw][gridz][gridy][gridx] = 0
                    else:
                        board[gridw][gridz][gridy][gridx] = (
                            board[gridw][gridz][gridy][gridx] ^ 1
                        )
                if event.mod != 0:
                    # if 1 == 1:
                    if event.key == K_UP and gridz > 0:
                        board[gridw][gridz][gridy][gridx] = (
                            board[gridw][gridz][gridy][gridx]
                        ) ^ 2
                        board[gridw][gridz - 1][gridy][gridx] = (
                            board[gridw][gridz - 1][gridy][gridx]
                        ) ^ 4
                    if event.key == K_DOWN and gridz + 1 < sizez:
                        board[gridw][gridz][gridy][gridx] = (
                            board[gridw][gridz][gridy][gridx]
                        ) ^ 4
                        board[gridw][gridz + 1][gridy][gridx] = (
                            board[gridw][gridz + 1][gridy][gridx]
                        ) ^ 2
                    if event.key == K_RIGHT and gridw + 1 < sizew:
                        board[gridw][gridz][gridy][gridx] = (
                            board[gridw][gridz][gridy][gridx]
                        ) ^ 8
                        board[gridw + 1][gridz][gridy][gridx] = (
                            board[gridw + 1][gridz][gridy][gridx]
                        ) ^ 16
                    if event.key == K_LEFT and gridw > 0:
                        board[gridw][gridz][gridy][gridx] = (
                            board[gridw][gridz][gridy][gridx]
                        ) ^ 16
                        board[gridw - 1][gridz][gridy][gridx] = (
                            board[gridw - 1][gridz][gridy][gridx]
                        ) ^ 8
                    if event.key == K_q:
                        board[gridw][gridz][gridy][gridx] = (
                            board[gridw][gridz][gridy][gridx]
                        ) ^ 32
                mreyes.update()
                mreyes.draw(DISPLAYSURF)
                # PrintBoard(board)
                DrawLayer(board, gridz, gridw)
                numtext = f"X={gridx}, Y={gridy}, Z={gridz}, W={gridw}, {gridx}/{gridy}/{gridz}/{gridw}"
                DrawText((GRIDSIZE * 5), (GRIDSIZE * 10 + 25), "ello there world")
                DrawText((GRIDSIZE * 5), (GRIDSIZE * 10 + 25), numtext)

        mreyes.draw(DISPLAYSURF)

        pygame.display.update()
        FramePerSec.tick(FPS)


# arrow graphics for d3, d4
aup = ((16, 14), (25, 5), (34, 14))
adown = ((34, 36), (25, 45), (16, 36))
aright = ((36, 16), (45, 25), (36, 34))
aleft = ((14, 34), (5, 25), (14, 16))


def DrawArrow(x, y, scale, color, points):
    pts = []
    for p in points:
        pts.append( (int(p[0] * scale + x), int(p[1] * scale + y)) )
    pygame.draw.polygon(DISPLAYSURF, color, pts, 2)


def DrawLayer2(board, z, w, px, py, scale):
    layer = board[w][z]
    size = int(GRIDSIZE * scale)
    for y in range(len(layer)):
        row = layer[y]
        for x in range(len(row)):
            if layer[y][x] == 0:
                pygame.draw.rect(
                    DISPLAYSURF, BLACK, Rect(px + size * x, py + size * y, size, size)
                )
            else:
                pygame.draw.rect(
                    DISPLAYSURF, WHITE, Rect(px + size * x, py + size * y, size, size)
                )
                if layer[y][x] & 2:
                    DrawArrow(px + size * x, py + size * y, scale, RED, aup)
                    # pygame.draw.polygon(DISPLAYSURF, RED, ((x*GRIDSIZE+16, y*GRIDSIZE+14), (x*GRIDSIZE+25, y*GRIDSIZE+5), (x*GRIDSIZE+34, y*GRIDSIZE+14)), 2)
                if layer[y][x] & 4:
                    DrawArrow(px + size * x, py + size * y, scale, GREEN, adown)
                if layer[y][x] & 8:
                    DrawArrow(px + size * x, py + size * y, scale, BLUE, aright)
                if layer[y][x] & 16:
                    DrawArrow(px + size * x, py + size * y, scale, PURPLE, aleft)


def DrawOverview(board):
    scale = 0.3
    DISPLAYSURF.fill(GRaY)
    for i in range(sizew):
        px = i * GRIDSIZE * scale * (sizex + 1)
        for j in range(sizez):
            py = j * GRIDSIZE * scale * (sizey + 1)
            DrawLayer2(board, j, i, px, py, scale)

def Overview(board):
    DrawOverview(board)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                DISPLAYSURF.fill(GRaY)
                return
        pygame.display.update()
        FramePerSec.tick(FPS)


def TunnelWorm(board, n):
    global gridx, gridy, gridz, gridw

    def negate(vector):
        v2 = [-x for x in vector]
        return v2

    def add(v1, v2):
        v3 = list(map(operator.add, v1, v2))
        return v3

    def inrange(v):
        return (
            all([a >= 0 for a in v])
            and v[0] < sizex
            and v[1] < sizey
            and v[2] < sizez
            and v[3] < sizew
        )

    # each dimension represented according to its extent,
    # favoring that ones with the larger size
    # increasing a decreases the favoring
    sizes = (sizex, sizey, sizez, sizew)
    a = 2
    dims = ((sizex+a) * [0] + (sizey+a) * [1] + (sizez+a) * [2] +  (sizew+a) * [3])
    dsize = len(dims)

    moves = (
        [1, 0, 0, 0], 
        [0, 1, 0, 0], 
        [0, 0, 1, 0], 
        [0, 0, 0, 1]       
    )

    prevmove = [0, 0, 0, 0]
    # represent position as a vector for convenience:
    position = [gridx, gridy, gridz, gridw]
    for i in range(n):
        while True:  # repeat ... until move != negate(prevmove)
            j = randrange(0, dsize)
            d = dims[j]          # which dimension
            k = randrange(0, 2)  # + or - direction
            move = moves[d]
            if k == 1: move = negate(move)
            if move != negate(prevmove):
                break
        # now we have a move that is not the direct inverse of the previous move
        target = add(position, move)
        if not inrange(target):
            # rather than cross the boundary, go the other way:
            move = negate(move)
        # It is helpful to go on straight runs in the larger dimensions to avoid
        # staying tightly packed in one area:
        steps = randint(1, sizes[d] // 3)
        for s in range(steps):
            target = add(position, move)
            if not inrange(target): break  # stop if hit edge, can't happen 1st time
            gx, gy, gz, gw = target  # the new location

            #!!! imperfection: assuming no more than one step in z or w
            if board[gw][gz][gy][gx] == 0:
                # here is where we tunnel: open up one blocked space
                board[gw][gz][gy][gx] = 1
            if move[2] > 0:
                board[gw][gz][gy][gx] |= 2
                board[gridw][gridz][gridy][gridx] |= 4
            if move[2] < 0:
                board[gw][gz][gy][gx] |= 4
                board[gridw][gridz][gridy][gridx] |= 2
            if move[3] > 0:
                board[gw][gz][gy][gx] |= 16
                board[gridw][gridz][gridy][gridx] |= 8
            if move[3] < 0:
                board[gw][gz][gy][gx] |= 8
                board[gridw][gridz][gridy][gridx] |= 16
            position = target
            gridx, gridy, gridz, gridw = target
        prevmove = move

        # the following allows this to be a long running, updating loop
        # while keeping the operating system happy
        DrawOverview(board)
        pygame.display.update()
        FramePerSec.tick(2)
        events = pygame.event.get()
        if events: 
            event = events[0]
            if event.type == KEYDOWN and  event.key == K_ESC:
                return

main()
