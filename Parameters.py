import pygame
import time

# Paramters for map
NUM_TRY20 = 1
NUM_TRY40 = 0
NUM_TRY60 = 0
RUNS20 = 10
RUNS40 = 100
RUNS60 = 5000

NUM_HOUSES20 = 20
NUM_HOUSES40 = 40
NUM_HOUSES60 = 60
MARGIN = 0.995

B3 = 11
L3 = 10.5

# Parameters for saving data
SAVE_PATH_PNG = 'C:\Users\Tom\PycharmProjects\heuristieken\Images'
SAVE_PATH_CSV = 'C:\Users\Tom\PycharmProjects\heuristieken\CSV'

# Parameters for visualization in pygame
PAR = 3
pygame.init()
MAP_X = 150
MAP_Y = 160
WHITE = (255, 255, 255)
INDIAN = (205, 85,	85)
RED = (204, 0, 0)
MAROON = (128, 0, 0)
GREEN = (143, 188, 143)
BLUE = (13,	113, 198)
dflags = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE
screen = pygame.display.set_mode((MAP_X * PAR, MAP_Y * PAR), dflags)

