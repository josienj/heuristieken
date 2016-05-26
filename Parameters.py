import pygame


# Parameters for tries.
NUM_TRY20 = 7393
NUM_TRY40 = 10000
NUM_TRY60 = 10
# Paramters for runs.
RUNS20 = 0
RUNS40 = 0
RUNS60 = 1000

# Parameters for number of houses.
NUM_HOUSES20 = 20
NUM_HOUSES40 = 40
NUM_HOUSES60 = 60

# If CHECKED is true, hillclimber is used to increase total value of the map.
# If CHECKED is false, hillclimber is used to increase total distance of the map.
CHECKED = True

# Parameters for saving data
SAVE_PATH_PNG = 'C:\Users\Tom\PycharmProjects\heuristieken\Images'
SAVE_PATH_CSV = 'C:\Users\Tom\PycharmProjects\heuristieken\CSV'

# Parameters for visualization in pygame
PAR = 3
pygame.init()
MAP_X = 150
MAP_Y = 160
WHITE = (255, 255, 255)
INDIAN = (205, 85, 85)
RED = (204, 0, 0)
MAROON = (128, 0, 0)
GREEN = (143, 188, 143)
BLUE = (13, 113, 198)
dflags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
screen = pygame.display.set_mode((MAP_X * PAR, MAP_Y * PAR), dflags)

# Parameters for all housetypes.
PERCTYPE1 = 0.6
B1 = 8
L1 = 8
HOUSEFREE1 = 2
HOUSEVALUE1 = 285000
HOUSEPERC1 = 0.03
HOUSECOLOR1 = RED
PERCTYPE2 = 0.25
B2 = 10
L2 = 7.5
HOUSEFREE2 = 0.25
HOUSEVALUE2 = 399000
HOUSEPERC2 = 0.04
HOUSECOLOR2 = INDIAN
PERCTYPE3 = 0.15
B3 = 11
L3 = 10.5
HOUSEFREE3 = 6
HOUSEVALUE3 = 610000
HOUSEPERC3 = 0.06
HOUSECOLOR3 = MAROON