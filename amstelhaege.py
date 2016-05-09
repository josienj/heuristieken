import random
import math
import pygame

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (204, 0, 0)
GREEN = (0, 204, 0)
BLUE = (0, 0, 204)
PURPLE = (204, 0, 204)
dflags = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE
screen = pygame.display.set_mode((150, 160), dflags)
screen.fill(WHITE)
# rect1 = pygame.Rect(20, 20, 8, 8)
# pygame.draw.rect(screen, BLACK, rect1, 1)
# rect2 = pygame.draw.rect(screen, BLACK, [23, 23, 8, 8], 1)
pygame.display.update()


class House(object):
    def __init__(self, width, length, free, houses):
        self.basevalue = 0
        self.perc = 0.00
        self.width = width
        self.length = length
        self.free = free
        self.map = Map()
        listlength = len(houses)
        self.position = self.map.getrandom(self.width, self.length, self.free)
        getcoordinates(self)
        if listlength != 0:
            for i in range(listlength):
                while checkoverlap(self, houses[i], checkdistance(self, houses[i])) != False:
                    self.position = self.map.getrandom(self.width, self.length, self.free)
                    getcoordinates(self)
        self.rect = (self.pos_X_L, self.pos_Y_O, self.width, self.length)
        self.color = BLACK


class Map(object):
    def __init__(self):
        self.x_axis = 150
        self.y_axis = 160

    def getrandom(self, width, length, free):
        x = random.uniform((0 + free), (self.x_axis - (width + free)))
        y = random.uniform((0 + free), (self.y_axis - (length + free)))
        return x, y


def calculatemin_distance(house, houses, numhouses, housenumber):
    min_distance = house.pos_X_L
    if house.map.x_axis - house.pos_X_R < min_distance:
        min_distance = house.map.x_axis - house.pos_X_R
    if house.pos_Y_O < min_distance:
        min_distance = house.pos_Y_O
    if house.map.y_axis - house.pos_Y_B < min_distance:
        min_distance = house.map.y_axis - house.pos_Y_B
    for i in range(numhouses):
        if i == housenumber:
            continue
        tempdistance = checkdistance(house, houses[i])
        if min_distance <= 0:
            min_distance = tempdistance
        if tempdistance < min_distance:
            min_distance = tempdistance

    return min_distance


def calculatedistance(houses, numhouses):
    totaldistance = 0
    for i in range(numhouses):
        min_distance = calculatemin_distance(houses[i], houses, numhouses, i)
        totaldistance += min_distance

    return totaldistance


def calculatevalue(houses, numhouses):
    totalvalue = 0
    for i in range(numhouses):
        min_distance = calculatemin_distance(houses[i], houses, numhouses, i)
        totalvalue += houses[i].basevalue * (1 + (houses[i].perc * min_distance))

    return totalvalue


def checkoverlap(house, checkedhouse, distance):
    if distance < house.free or distance < checkedhouse.free:
        return True
    else:
        return False


def checkdistance(house, housechecked):
    XL1 = house.pos_X_L
    XR1 = house.pos_X_R
    YO1 = house.pos_Y_O
    YB1 = house.pos_Y_B
    XL2 = housechecked.pos_X_L
    XR2 = housechecked.pos_X_R
    YO2 = housechecked.pos_Y_O
    YB2 = housechecked.pos_Y_B

    if XL1 == XL2:
        distance = 0

    # If house and house[i] overlap on x-axis
    elif (XL1 > XL2 and XL1 < XR2 or XL2 > XL1 and XL2 < XR1):
        # If house is lower than house[i]
        if YO1 < YO2:
            distance = YO2 - YB1
        # If house is higher than house[i]
        elif YO1 > YO2:
            distance = YO1 - YB2

    # If house and house[i] overlap on y-axis
    elif (YO1 > YO2 and YO1 < YB2 or YO2 > YO1 and YO2 < YB1):
        # If house is lower than house[i]
        if XL1 > XL2:
            distance = XL1 - XR2
        # If house is higher than house[i]
        elif XL1 < XL2:
            distance = XL2 - XR1

    # If house is left of house[i]
    elif XL2 > XL1 and XL2 >= XR1:
        # If house is lower than house[i]
        if YO2 > YO1:
            dy = YO2 - YB1
            dx = XL2 - XR1
        # if house is higher than house[i]
        elif YO2 < YO1:
            dy = YO1 - YB2
            dx = XL2 - XR1
        distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

    # If house is right of house[i]
    elif XL2 < XL1 and XR2 <= XL1:
        # If house is lower than house[i]
        if YO2 > YO1:
            dy = YO2 - YB1
            dx = XL1 - XR2
        # If house is higher than house[i]
        elif YO2 < YO1:
            dy = YO1 - YB2
            dx = XL1 - XR2
        distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

    return distance


def getcoordinates(house):
    house.pos_X_L = house.position[0]
    house.pos_X_R = house.position[0] + house.width
    house.pos_Y_O = house.position[1]
    house.pos_Y_B = house.position[1] + house.length


def placehouses(numhouses):
    houses = []
    i = 0

    while i < (numhouses * 0.6):
        houses.append(House(8, 8, 2, houses))
        houses[i].basevalue = 285000
        houses[i].perc = 0.03
        houses[i].color = RED
        i += 1
    while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
        houses.append(House(10, 7.5, 3, houses))
        houses[i].basevalue = 399000
        houses[i].perc = 0.04
        houses[i].color = GREEN
        i += 1
    while i >= (numhouses * 0.85) and i < numhouses:
        houses.append(House(11, 10.5, 6, houses))
        houses[i].basevalue = 610000
        houses[i].perc = 0.06
        houses[i].color = PURPLE
        i += 1

        for i in range(numhouses):
            print numhouses
            print i
            for j in range(numhouses):
                print j
                if i == j:
                   continue
                distance = checkdistance(houses[i], houses[j])
                if checkoverlap(houses[i], houses[j], distance):
                    print "There is overlap between house", i, "and house", j
                    overlap = 1
                    while overlap == 1:
                        houses[i].position = houses[i].map.getrandom(houses[i].width, houses[i].length, houses[i].free)
                        getcoordinates(houses[i])
                        count = 0
                        for k in range(numhouses):
                            if i == k:
                                continue
                            distance = checkdistance(houses[i], houses[k])
                            if checkoverlap(houses[i], houses[k], distance) == False:
                                count += 1
                            if count == numhouses - 1:
                                overlap = 0




    return houses


def replacehouse(house, houses, numhouses, housenumber):
    # Calculations
    tempposition = house.position
    tempvalue = calculatevalue(houses, numhouses)
    totalvalue = tempvalue
    print totalvalue, "totalvalue before replacing"
    for i in range(numhouses):
        if i == housenumber:
            continue
        distance = checkdistance(house, houses[i])

    # Replacing and recalculating
    house.position = house.map.getrandom(house.width, house.length, house.free)
    getcoordinates(house)
    totalvalue = calculatevalue(houses, numhouses)
    print totalvalue, "totalvalueafter replacing"
    for i in range(numhouses):
        if i == housenumber:
            continue
        distance = checkdistance(house, houses[i])
        if checkoverlap(house, houses[i], distance):
            house.position = tempposition
            getcoordinates(house)

    if totalvalue < tempvalue:
        house.position = tempposition
        getcoordinates(house)

    houses[housenumber].position = house.position
    getcoordinates(houses[housenumber])
    houses[housenumber].rect = (house.pos_X_L, house.pos_Y_O, house.width, house.length)
    return houses

def run(numhouses):
    houses = placehouses(numhouses)
    for i in range(numhouses):
        pygame.draw.rect(screen, houses[i].color, houses[i].rect, 1)
    pygame.display.update()
    for i in range(50):
        for j in range(numhouses):
            pygame.draw.rect(screen, WHITE, houses[j].rect, 1)
            # pygame.time.delay(200)
            houses = replacehouse(houses[j], houses, numhouses, j)
            getcoordinates(houses[j])
            pygame.draw.rect(screen, houses[j].color, houses[j].rect, 1)
            pygame.display.update()
        totalvalue = calculatevalue(houses, numhouses)
        print "totavalue in run '#'",i, "= ", totalvalue


run = run(20)