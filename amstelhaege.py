import random
import math
import os
import os.path
import csv
import time

from Parameters import *

screen = pygame.display.set_mode(((MAP_X * PAR), (MAP_Y * PAR)), dflags)
screen.fill(GREEN)
pygame.display.update()


def run(numhouses, runs, tries):
    screen.fill(GREEN)
    pygame.display.update()
    runinfo = Info()
    map = Map()
    print "numwater =", NUM_WATER
    waters = placewater(NUM_WATER, map)
    time.sleep(10)
    for i in range(NUM_WATER):
        getcoordinateswater(waters[i])
        pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
        pygame.display.update()
    houses = placehouses(numhouses, map)
    for i in range(numhouses):
        pygame.draw.rect(screen, houses[i].color, houses[i].rect, 0)
    pygame.display.update()
    for i in range(runs):
        for j in range(numhouses):
            pygame.draw.rect(screen, GREEN, houses[j].rect, 0)
            houses = replacehouse(houses[j], houses, numhouses, i)
            getcoordinateshouse(houses[j])
            pygame.draw.rect(screen, houses[j].color, houses[j].rect, 0)
            pygame.display.update()
        totalvalue = calculatevalue(houses, numhouses)
        print tries, "run '#'", i, "= ", totalvalue
    pygame.image.save(screen, 'output.png')
    totalvalue = calculatevalue(houses, numhouses)
    totaldistance = calculatedistance(houses, numhouses)
    save(numhouses, runs, totalvalue, totaldistance, screen)
    time.sleep(20)

# T = c / log(1+iteraties)

#####
# A Class in which the values of the house are first created and stored.
# The values 'basevalue', 'perc' and 'color' are different for each house type.
# These values are added seperately, later in placeHouses.
#####


class House(object):
    def __init__(self, width, length, free, houses, map):
        self.basevalue = 0
        self.perc = 0.00
        self.width = width
        self.length = length
        self.free = free
        self.map = map
        self.position = self.map.getrandom(self.width, self.length, self.free)
        listlength = len(houses)
        self.pos_X_L = 0
        self.pos_X_R = 0
        self.pos_Y_O = 0
        self.pos_Y_B = 0
        getcoordinateshouse(self)
        if listlength != 0:
            for i in range(listlength):
                while checkoverlap(self, houses[i], checkdistance(self, houses[i])) != False:
                    self.position = self.map.getrandom(self.width, self.length, self.free)
                    getcoordinateshouse(self)
        self.rect = ((self.pos_X_L * PAR), (self.pos_Y_O * PAR), (self.width * PAR), (self.length * PAR))
        self.color = WHITE


class Water(object):
    def __init__(self, map):
        x = random.randint(1, 4)
        print "x =", x
        y = random.randint(0, 1)
        print "y =", y
        self.surface = 0
        while self.surface == 0:
            if map.waterbodies < (NUM_WATER - 1):
                self.surface = random.uniform(0, map.remainingsurface)
            else:
                self.surface = map.remainingsurface
        map.waterbodies += 1
        print "self.surface =", self.surface
        map.remainingsurface -= self.surface
        print "water remaining =", map.remainingsurface
        if y == 0:
            self.width =
            self.length = 
        if y == 1:
            self.length =
            self.width =
        print "width =", self.width
        print "length =", self.length
        self.position = map.getrandom(self.width, self.length, 0)
        print self.position
        self.pos_X_L = self.position[0]
        self.pos_X_R = self.position[0] + self.width
        self.pos_Y_O = self.position[1]
        self.pos_Y_B = self.position[1] + self.length
        print "watercoord = ", self.pos_X_L, self.pos_Y_O
        getcoordinateswater(self)
        self.rect = ((self.pos_X_L * PAR), (self.pos_Y_O * PAR), (self.width * PAR), (self.length * PAR))
        self.color = BLUE


class Info(object):
    def __init__(self):
        self.nochange = 0
        self.firstswap = 1
        self.besthouses = []
        self.bestvalue = 0


class Map(object):
    def __init__(self):
        self.x_axis = MAP_X
        self.y_axis = MAP_Y

        self.watersurface = (self.x_axis * self.y_axis * 0.2)
        print "watersurface =", self.watersurface
        self.remainingsurface = self.watersurface
        print "remainingsurface =", self.remainingsurface
        self.waterbodies = 0
        print "waterbodies =", self.waterbodies

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
        min_distance = calculatemin_distance(houses[i], houses, numhouses, i) - houses[i].free
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
    elif YO1 > YO2 and YO1 < YB2 or YO2 > YO1 and YO2 < YB1:
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


def getcoordinateshouse(house):
    house.pos_X_L = house.position[0]
    house.pos_X_R = house.position[0] + house.width
    house.pos_Y_O = house.position[1]
    house.pos_Y_B = house.position[1] + house.length

    return house


def getcoordinateswater(water):
    water.pos_X_L = water.position[0]
    water.pos_X_R = water.position[0] + water.width
    water.pos_Y_O = water.position[1]
    water.pos_Y_B = water.position[1] + water.length

    return water


def placewater(numwater, map):
    waters = []
    i = numwater
    while i > 0:
        waters.append(Water(map))
        i -= 1

    print waters
    return waters


def placehouses(numhouses, map):
    houses = []
    i = 0

    while i < (numhouses * 0.6):
        houses.append(House(8, 8, 2, houses, map))
        houses[i].basevalue = 285000
        houses[i].perc = 0.03
        houses[i].color = RED
        i += 1
    while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
        houses.append(House(10, 7.5, 3, houses, map))
        houses[i].basevalue = 399000
        houses[i].perc = 0.04
        houses[i].color = INDIAN
        i += 1
    while i >= (numhouses * 0.85) and i < numhouses:
        houses.append(House(11, 10.5, 6, houses, map))
        houses[i].basevalue = 610000
        houses[i].perc = 0.06
        houses[i].color = MAROON
        i += 1

    for i in range(numhouses):
        for j in range(numhouses):
            if i == j:
                continue
            distance = checkdistance(houses[i], houses[j])
            if checkoverlap(houses[i], houses[j], distance):
                for x in range(numhouses):
                    pygame.draw.rect(screen, houses[x].color, houses[x].rect, 0)
                    pygame.display.update()
                overlap = 1
                while overlap == 1:
                    houses[i].position = houses[i].map.getrandom(houses[i].width, houses[i].length, houses[i].free)
                    getcoordinateshouse(houses[i])
                    count = 0
                    for k in range(numhouses):
                        if i == k:
                            continue
                        distance = checkdistance(houses[i], houses[k])
                        if not checkoverlap(houses[i], houses[k], distance):
                            count += 1
                        if count == numhouses - 1:
                            overlap = 0

    return houses


def replacehouse(house, houses, numhouses, housenumber):
    oldposition = house.position
    oldvalue = calculatevalue(houses, numhouses)

    house.position = house.map.getrandom(house.width, house.length, house.free)
    getcoordinateshouse(house)
    for i in range(numhouses):
        if i == housenumber:
            continue
        while True:
            counter = 0
            for j in range(numhouses):
                if j == housenumber:
                    continue
                if checkoverlap(house, houses[j], checkdistance(house, houses[j])):
                    house.position = house.map.getrandom(house.width, house.length, house.free)
                    getcoordinateshouse(house)
                    break
                else:
                    counter += 1
            if counter == numhouses - 1:
                break

    houses[housenumber].position = house.position
    getcoordinateshouse(houses[housenumber])
    totalvalue = calculatevalue(houses, numhouses)

    if totalvalue <= oldvalue:
        house.position = oldposition
        getcoordinateshouse(house)

    houses[housenumber].position = house.position
    getcoordinateshouse(houses[housenumber])
    houses[housenumber].rect = ((house.pos_X_L * PAR), (house.pos_Y_O * PAR),
                                (house.width * PAR), (house.length * PAR))
    return houses


def save(numhouses, runs, totalvalue, totaldistance, screen):
    pngcount = 0
    while os.path.exists("Images\output%s.png" % pngcount):
        pngcount += 1
    outputfinal = os.path.join(SAVE_PATH_PNG, 'output'+pngcount.__str__())
    pygame.image.save(screen, outputfinal+'.png')

    csvcount = 0
    while os.path.exists("output%s.csv" % csvcount):
        csvcount += 1
    # outputfinal = os.path.join(SAVE_PATH_CSV, 'output'+csvcount.__str__())

    csvstring = ['output'+tries.__str__(), numhouses, runs, totalvalue, totaldistance]

    with open('total.csv', "a") as writefile:
        writer = csv.writer(writefile, delimiter=',', quotechar="'", lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerow(csvstring)

    writefile.close()


i = 0
j = 0
k = 0
tries = 0
while i < NUM_TRY20:
    run(NUM_HOUSES20, RUNS20, tries)
    i += 1
    tries += 1
while j < NUM_TRY40:
    run(NUM_HOUSES40, RUNS40, tries)
    j += 1
    tries += 1
while k < NUM_TRY60:
    run(NUM_HOUSES60, RUNS60, tries)
    k += 1
    tries += 1
