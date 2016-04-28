import random
import math


class House(object):
    def __init__(self, width, length, free):
        self.basevalue = 0
        self.perc = 0.00
        self.width = width
        self.length = length
        self.free = free
        self.map = Map()
        self.position = self.map.getrandom(self.width, self.length, self.free)
        self.pos_X_L = self.position[0]
        self.pos_X_R = self.position[0] + width
        self.pos_Y_O = self.position[1]
        self.pos_Y_B = self.position[1] + length


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


def placehouses(numhouses):
    houses = []
    i = 0
    while i < (numhouses * 0.6):
        houses.append(House(8, 8, 2))
        houses[i].basevalue = 285000
        houses[i].perc = 0.03
        i += 1
    while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
        houses.append(House(10, 7.5, 3))
        houses[i].basevalue = 399000
        houses[i].perc = 0.04
        i += 1
    while i >= (numhouses * 0.85) and i < numhouses:
        houses.append(House(11, 10.5, 6))
        houses[i].basevalue = 610000
        houses[i].perc = 0.06
        i += 1
    return houses


def replacehouse(house, houses, numhouses, housenumber):
    # print house.position
    tempposition = house.position
    tempvalue = calculatevalue(houses, numhouses)
    house.position = house.map.getrandom(house.width, house.length, house.free)
    if calculatevalue(houses, numhouses) < tempvalue:
        house.position = tempposition
    else:
        for i in range(numhouses):
            if i != housenumber:
                distance = checkdistance(house, houses[i])
                if checkoverlap(house, houses[i], distance):
                    house.position = tempposition
                    break
            else:
                continue
    # print house.position
    # print calculatevalue(houses, numhouses)
    return house

def run(numhouses):
    houses = placehouses(numhouses)
    for i in range(1000):
        for j in range(numhouses):
            houses[j] = replacehouse(houses[j], houses, numhouses, j)
            print calculatevalue(houses, numhouses)
            print houses[0].position, houses[1].position, houses[2].position

run = run(3)