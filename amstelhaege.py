import math
import os
import os.path
import csv
import time
import random
import time

from Parameters import *
# T = c / log(1+iteraties)


def run(numhouses, numwaters, runs, attempts):
    screen.fill(GREEN)
    pygame.display.update()
    mapwater = Map()
    waters = placewater(numwaters, mapwater, screen)
    houses = placehouses(numhouses, numwaters, waters)
    for i in range(numwaters):
        pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
    pygame.display.update()
    for i in range(numhouses):
        pygame.draw.rect(screen, houses[i].color, houses[i].rect, 0)
    pygame.display.update()
    for j in range(runs):
        for i in range(numwaters):
            pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
        for k in range(numhouses):
            pygame.draw.rect(screen, GREEN, houses[k].rect, 0)
            houses = replacehouse(houses[k], houses, numhouses, k)
            getcoordinates(houses[k])
            houses[k].rect = (houses[k].pos_x_l * PAR, houses[k].pos_y_l * PAR,
                              houses[k].width * PAR, houses[k].length * PAR)
            pygame.draw.rect(screen, houses[k].color, houses[k].rect, 0)
            pygame.display.update()
        totalvalue = calculatevalue(houses, numhouses)
        print attempts, "totavalue in run '#'", j, "= ", totalvalue
    screen.fill(GREEN)
    for i in range(numwaters):
        pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
    for i in range(numhouses):
        pygame.draw.rect(screen, houses[i].color, houses[i].rect, 0)
    pygame.display.update()
    pygame.image.save(screen, 'output.png')
    totalvalue = calculatevalue(houses, numhouses)
    totaldistance = calculatedistance(houses, numhouses)
    save(numhouses, numwaters, houses, waters, runs, totalvalue, totaldistance, screen)


#####
# A Class in which the values of the house are first created and stored.
# The values 'basevalue', 'perc' and 'color' are different for each house type.
# These values are added seperately, later in placeHouses.
#####
class House(object):
    def __init__(self, width, length, free, houses):
        self.basevalue = 0
        self.perc = 0.00
        self.width = width
        self.length = length
        self.free = free
        self.map = Map()
        self.position = self.map.getrandom(self.width, self.length, self.free)
        self.pos_x_l = 0
        self.pos_x_r = 0
        self.pos_y_l = 0
        self.pos_y_u = 0
        getcoordinates(self)
        self.rect = (self.pos_x_l * PAR, self.pos_y_l * PAR,
                     self.width * PAR, self.length * PAR)
        self.color = GREEN


class Water(object):
    def __init__(self, mapwater):
        if mapwater.waterbodies < (NUM_WATER - 1):
            self.surface = random.uniform(0, mapwater.remainingsurface)
        else:
            self.surface = mapwater.remainingsurface
        mapwater.remainingsurface -= self.surface
        mapwater.waterbodies += 1
        rand = random.randint(0, 1)
        if rand == 0:
            self.width = random.uniform(math.sqrt(self.surface), (2 * math.sqrt(self.surface)))
            self.length = self.surface / self.width
        if rand == 1:
            self.length = random.uniform(math.sqrt(self.surface), (2 * math.sqrt(self.surface)))
            self.width = self.surface / self.length
        self.position = mapwater.getrandom(self.width, self.length, 0)
        self.pos_x_l = 0
        self.pos_x_r = 0
        self.pos_y_l = 0
        self.pos_y_u = 0
        getcoordinateswater(self)
        self.rect = ((self.pos_x_l * PAR), (self.pos_y_l * PAR),
                     (self.width * PAR), (self.length * PAR))
        self.color = BLUE


class Map(object):
    def __init__(self):
        self.x_axis = MAP_X
        self.y_axis = MAP_Y

        self.totalwater = (MAP_X * MAP_Y) * 0.2
        self.waterbodies = 0
        self.remainingsurface = self.totalwater

    def getrandom(self, width, length, free):
        x = random.uniform((0 + free), (self.x_axis - (width + free)))
        y = random.uniform((0 + free), (self.y_axis - (length + free)))
        return x, y


def calculatemin_distance(house, houses, numhouses, housenumber):
    min_distance = house.pos_x_l
    if house.map.x_axis - house.pos_x_r < min_distance:
        min_distance = house.map.x_axis - house.pos_x_r
    if house.pos_y_l < min_distance:
        min_distance = house.pos_y_l
    if house.map.y_axis - house.pos_y_u < min_distance:
        min_distance = house.map.y_axis - house.pos_y_u
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


def checkoverlapwater(house, water, numwaters):
    if checkdistance(house, water) < 0:
            return True

    return False


def checkdistance(house, housechecked):
    x1l = house.pos_x_l
    x1r = house.pos_x_r
    y1l = house.pos_y_l
    y1u = house.pos_y_u
    x2l = housechecked.pos_x_l
    x2r = housechecked.pos_x_r
    y2l = housechecked.pos_y_l
    y2u = housechecked.pos_y_u

    dx = 0
    dy = 0
    distance = 0

    if x1l == x2l:
        distance = 0

    # If house and house[i] overlap on x-axis
    elif x2l < x1l < x2r or x2l > x1l and x1r > x2l:
        # If house is lower than house[i]
        if y1l < y2l:
            distance = y2l - y1u
        # If house is higher than house[i]
        elif y1l > y2l:
            distance = y1l - y2u

    # If house and house[i] overlap on y-axis
    elif y2l < y1l < y2u or y2l > y1l and y1u > y2l:
        # If house is lower than house[i]
        if x1l > x2l:
            distance = x1l - x2r
        # If house is higher than house[i]
        elif x1l < x2l:
            distance = x2l - x1r

    # If house is left of house[i]
    elif x2l > x1l and x1r <= x2l:
        # If house is lower than house[i]
        if y2l > y1l:
            dy = y2l - y1u
            dx = x2l - x1r
        # if house is higher than house[i]
        elif y2l < y1l:
            dy = y1l - y2u
            dx = x2l - x1r
        distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

    # If house is right of house[i]
    elif x2l < x1l and x2r <= x1l:
        # If house is lower than house[i]
        if y2l > y1l:
            dy = y2l - y1u
            dx = x1l - x2r
        # If house is higher than house[i]
        elif y2l < y1l:
            dy = y1l - y2u
            dx = x1l - x2r
        distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

    return distance


def getcoordinates(house):
    house.pos_x_l = house.position[0]
    house.pos_x_r = house.position[0] + house.width
    house.pos_y_l = house.position[1]
    house.pos_y_u = house.position[1] + house.length


def getcoordinateswater(water):
    water.pos_x_l = water.position[0]
    water.pos_x_r = water.position[0] + water.width
    water.pos_y_l = water.position[1]
    water.pos_y_u = water.position[1] + water.length


def placehouses(numhouses, numwaters, waters):
    houses = []
    i = 0

    while i < (numhouses * 0.6):
        houses.append(House(8, 8, 2, houses))
        houses[i].basevalue = 285000
        houses[i].perc = 0.03
        houses[i].color = RED
        i += 1
    while (numhouses * 0.6) <= i < (numhouses * 0.85):
        houses.append(House(10, 7.5, 3, houses))
        houses[i].basevalue = 399000
        houses[i].perc = 0.04
        houses[i].color = INDIAN
        i += 1
    while (numhouses * 0.85) <= i < numhouses:
        houses.append(House(11, 10.5, 6, houses))
        houses[i].basevalue = 610000
        houses[i].perc = 0.06
        houses[i].color = MAROON
        i += 1

    for x in range(numhouses):
        pygame.draw.rect(screen, houses[x].color, houses[x].rect, 0)
    pygame.display.update()

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
                    getcoordinates(houses[i])
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


def placewater(numwater, mapwater, screen):
    waters = []
    i = numwater
    while i > 0:
        waters.append(Water(mapwater))
        i -= 1

    for i in range(numwater):
        for j in range(numwater):
            if i == j:
                continue
            overlap = 0
            for k in range(numwater):
                if checkoverlapwater(waters[i], waters[k], numwater):
                    overlap = 1
            while overlap == 1:
                waters[i].position = mapwater.getrandom(
                    waters[i].width, waters[i].length, 0)
                getcoordinates(waters[i])
                waters[i].rect = (waters[i].pos_x_l * PAR, waters[i].pos_y_l * PAR,
                                  waters[i].width * PAR, waters[i].length * PAR)
                count = 0
                for l in range(numwater):
                    if i == l:
                        continue
                    if not checkoverlapwater(waters[i], waters[l], numwater):
                        count += 1
                    if count == numwater - 1:
                        overlap = 0

    screen.fill(GREEN)
    for i in range(numwater):
        pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
    pygame.display.update()
    return waters


def replacehouse(house, houses, numhouses, housenumber):
    # Calculations
    oldposition = house.position
    oldvalue = calculatevalue(houses, numhouses)

    # Replacing and recalculating
    house.position = house.map.getrandom(house.width, house.length, house.free)
    getcoordinates(house)
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
                    getcoordinates(house)
                    break
                else:
                    counter += 1
            if counter == numhouses - 1:
                break

    houses[housenumber].position = house.position
    getcoordinates(houses[housenumber])
    totalvalue = calculatevalue(houses, numhouses)

    if totalvalue <= oldvalue:
        house.position = oldposition
        getcoordinates(house)

    houses[housenumber].position = house.position
    getcoordinates(houses[housenumber])
    houses[housenumber].rect = (house.pos_x_l, house.pos_y_l, house.width, house.length)
    return houses


def save(numhouses, numwaters, houses, waters, runs, totalvalue, totaldistance, screen):

    # Finds existing csv files and assures no file is overwritten
    pngcount = 0
    while os.path.exists("Images\output%s.png" % pngcount):
        pngcount += 1
    # Print visual outcome of run in image file
    outputfinal = os.path.join(SAVE_PATH_PNG, 'output' + pngcount.__str__())
    pygame.image.save(screen, outputfinal + '.png')

    # Finds existing csv files and assures no file is overwritten
    csvcount = 0
    while os.path.exists("CSV\output%s.csv" % csvcount):
        csvcount += 1
    # Print details of outcome of run in csv file
    with open("CSV\output%s.csv" % csvcount, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL)
        writer.writerow(["numhouses", "runs", "totalvalue", "totaldistance"])
        writer.writerow([numhouses, runs, totalvalue, totaldistance])
        writer.writerow(["\n"])
        writer.writerow(["water", "position", "width", "length"])
        for i in range(numwaters):
            writer.writerow(["water" + i.__str__(), waters[i].position, waters[i].width, waters[i].length])
        writer.writerow(["\n"])
        writer.writerow(["house", "position", "width", "length", "free"])
        for j in range(numhouses):
            writer.writerow(["house" + j.__str__(), houses[j].position, houses[j].width, houses[j].length,
                            houses[j].free])
    csvfile.close()

    # Print results of run in total.csv
    with open('total.csv', "a") as writefile:
        writer = csv.writer(writefile, delimiter=',', quotechar="'", lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerow([numhouses, numwaters, runs, totalvalue, totaldistance, "output%s.csv" % csvcount,
                         "output%s.png" % pngcount])
    writefile.close()


i = 0
j = 0
k = 0
TRY = 0
while i < NUM_TRY20:
    NUM_WATER = random.randint(1, 4)
    run(NUM_HOUSES20, NUM_WATER, RUNS20, TRY)
    i += 1
    TRY += 1
while j < NUM_TRY40:
    NUM_WATER = random.randint(1, 4)
    run(NUM_HOUSES40, NUM_WATER, RUNS40, TRY)
    j += 1
    TRY += 1
while k < NUM_TRY60:
    NUM_WATER = random.randint(1, 4)
    run(NUM_HOUSES60, NUM_WATER, RUNS60, TRY)
    k += 1
    TRY += 1
