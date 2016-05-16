import math
import os
import os.path
import csv

from Parameters import *

# T = c / log(1+iteraties)

screen = pygame.display.set_mode((MAP_X * PAR, MAP_Y * PAR), dflags)
screen.fill(WHITE)
pygame.display.update()

SAVE_PATH_PNG = 'C:\Users\Tom\PycharmProjects\heuristieken\Images'
SAVE_PATH_CSV = 'C:\Users\Tom\PycharmProjects\heuristieken\CSV'


def run(numhouses, runs, attempts):
    screen.fill(GREEN)
    pygame.display.update()
    houses = placehouses(numhouses)
    for i in range(numhouses):
        pygame.draw.rect(screen, houses[i].color, houses[i].rect, 0)
    pygame.display.update()
    for j in range(runs):
        for k in range(numhouses):
            pygame.draw.rect(screen, GREEN, houses[k].rect, 0)
            houses = replacehouse(houses[k], houses, numhouses, k)
            getcoordinates(houses[k])
            houses[k].rect = (houses[k].pos_X_L * PAR, houses[k].pos_Y_O * PAR,
                              houses[k].width * PAR, houses[k].length * PAR)
            pygame.draw.rect(screen, houses[k].color, houses[k].rect, 0)
            pygame.display.update()
        totalvalue = calculatevalue(houses, numhouses)
        print attempts, "totavalue in run '#'", j, "= ", totalvalue
    pygame.image.save(screen, 'output.png')
    totalvalue = calculatevalue(houses, numhouses)
    totaldistance = calculatedistance(houses, numhouses)
    save(numhouses, runs, totalvalue, totaldistance, screen)


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
        self.pos_X_L = self.position[0]
        self.pos_X_R = self.position[0] + self.width
        self.pos_Y_O = self.position[1]
        self.pos_Y_B = self.position[1] + self.length
        listlength = len(houses)
        getcoordinates(self)
        if listlength != 0:
            for i in range(listlength):
                while checkoverlap(self, houses[i], checkdistance(self, houses[i])):
                    self.position = self.map.getrandom(self.width, self.length, self.free)
                    getcoordinates(self)
        self.rect = (self.pos_X_L * PAR, self.pos_Y_O * PAR,
                     self.width * PAR, self.length * PAR)
        self.color = GREEN


class Map(object):
    def __init__(self):
        self.x_axis = MAP_X
        self.y_axis = MAP_Y

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

    dx = 0
    dy = 0
    distance = 0

    if XL1 == XL2:
        distance = 0

    # If house and house[i] overlap on x-axis
    elif XL2 < XL1 < XR2 or XL2 > XL1 and XL2 < XR1:
        # If house is lower than house[i]
        if YO1 < YO2:
            distance = YO2 - YB1
        # If house is higher than house[i]
        elif YO1 > YO2:
            distance = YO1 - YB2

    # If house and house[i] overlap on y-axis
    elif YO2 < YO1 < YB2 or YO2 > YO1 and YO2 < YB1:
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
    houses[housenumber].rect = (house.pos_X_L, house.pos_Y_O, house.width, house.length)
    return houses


def save(numhouses, runs, totalvalue, totaldistance, screen):
    pngcount = 0
    while os.path.exists("Images\output%s.png" % pngcount):
        pngcount += 1
    outputfinal = os.path.join(SAVE_PATH_PNG, 'output' + pngcount.__str__())
    pygame.image.save(screen, outputfinal + '.png')

    csvcount = 0
    while os.path.exists("output%s.csv" % csvcount):
        csvcount += 1
    # outputfinal = os.path.join(SAVE_PATH_CSV, 'output' + csvcount.__str__())

    csvstring = ['output' + TRY.__str__(), numhouses, runs, totalvalue, totaldistance]

    with open('total.csv', "a") as writefile:
        writer = csv.writer(writefile, delimiter=',', quotechar="'", lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerow(csvstring)

    writefile.close()


i = 0
j = 0
k = 0
TRY = 0
while i < NUM_TRY20:
    run(NUM_HOUSES20, RUNS20, TRY)
    i += 1
    TRY += 1
while j < NUM_TRY40:
    run(NUM_HOUSES40, RUNS40, TRY)
    j += 1
    TRY += 1
while k < NUM_TRY60:
    run(NUM_HOUSES60, RUNS60, TRY)
    k += 1
    TRY += 1
