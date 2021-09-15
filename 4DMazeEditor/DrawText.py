import pygame, sys
from pygame.locals import *
import random
from tkinter import *
import tkinter.filedialog, tkinter.messagebox

# Initialize program
Tk().withdraw()
pygame.init()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define grid coords and grid size
gridx = 0
gridy = 0
gridz = 0
gridw = 0
GRIDSIZE = 50

# Setup a 300x300 pixel display with caption
DISPLAYSURF = pygame.display.set_mode(((GRIDSIZE*10),(GRIDSIZE*10+50)))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("It's 4D!")
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

def DrawText(x, y, txt):
    font = pygame.font.Font('arial.ttf', 32)
    
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render(txt, True, GREEN, BLUE)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (x // 2, y // 2)

    DISPLAYSURF.blit(text, textRect)

DrawText((GRIDSIZE*5), (GRIDSIZE), "ello there world")

while True:
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:

            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        # Draws the surface object to the screen.
        pygame.display.update()