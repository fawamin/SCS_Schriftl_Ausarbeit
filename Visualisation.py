import numpy as np
import pygame
import sys

from GameOfLife import GameOfLife
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)

pygame.init()
SCREEN_Width = 600
SCREEN_Height = 600
screen = pygame.display.set_mode((SCREEN_Width, SCREEN_Height))


class DisplayGOL:

    gol = None
    dw = None
    dh = None
    coldead = (255,255,255)
    colalive = (0,0,0)

    def __init__(self,displaywidth,displayheight):
        self.gol = GameOfLife()
        self.dw = displaywidth
        self.dh = displayheight

    def TestPeparationMethod(self):
        self.gol.setSaveFile("Saves/10x10Glider.npy")
        self.gol.loadFileData() 
        #DAYEVENT is event type thats user generated
        DAYEVENT  = pygame.USEREVENT+1
        # cyclelenght is the lenght in ms 
        cyclelenght = 500
        # Sets a Timer that triggers the DAYEVENT every cyclelenght ms
        pygame.time.set_timer(DAYEVENT,cyclelenght)
        running = True
        #Render Screen once before first Cycle
        self.renderScreen()
        while running:
            self.renderScreen()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
                if event.type == DAYEVENT:
                    self.gol.cycleDay()
                    self.renderScreen()



    def renderScreen(self):
        screen.fill((255, 255, 255))
        field = self.gol.getField()
        rows, cols = field.shape
        # Find Width and Height of each Square
        width = self.dw / rows
        height = self.dh / cols
        for row, col in np.ndindex(field.shape):
            #Is Cell Dead or Alive?
            if field[row,col] == 0:
                colour = self.coldead
            elif field[row,col] == 1:
                colour = self.colalive
            #Draw Cell
            pygame.draw.rect(screen,colour,(row * width - 2 ,col * height -2 , width -2 , height- 2))
        #Update display
        pygame.display.update()



di = DisplayGOL(SCREEN_Width,SCREEN_Height)
di.TestPeparationMethod()
