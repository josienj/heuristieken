import random
import math


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
        if listlength != 0:
            for i in range(listlength):
                while checkoverlap(self, houses[i], checkdistance(self, houses[i])) != False:
                    self.position = self.map.getrandom(self.width, self.length, self.free)
        self.pos_X_L = self.position[0]
        self.pos_X_R = self.position[0] + self.width
        self.pos_Y_O = self.position[1]
        self.pos_Y_B = self.position[1] + self.length


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
        i += 1
    while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
        houses.append(House(10, 7.5, 3, houses))
        houses[i].basevalue = 399000
        houses[i].perc = 0.04
        i += 1
    while i >= (numhouses * 0.85) and i < numhouses:
        houses.append(House(11, 10.5, 6, houses))
        houses[i].basevalue = 610000
        houses[i].perc = 0.06
        i += 1

    return houses


def replacehouse(house, houses, numhouses, housenumber):
    tempposition = house.position
    tempvalue = calculatevalue(houses, numhouses)
    house.position = house.map.getrandom(house.width, house.length, house.free)
    getcoordinates(house)
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

    houses[housenumber].position = house.position
    return houses

def run(numhouses):
    houses = placehouses(numhouses)
    totalvalue = calculatevalue(houses, numhouses)
    for i in range(numhouses):
        for j in range(numhouses):
            if i != j:
                if checkoverlap(houses[i], houses[j], checkdistance(houses[i], houses[j])):
                    print "There is overlap"
    for i in range(100):
        for j in range(numhouses):
            houses = replacehouse(houses[j], houses, numhouses, j)
            getcoordinates(houses[j])
            totalvalue = calculatevalue(houses, numhouses)
        print "totavalue in run '#'",i, "= ", totalvalue
    for i in range(numhouses):
        for j in range(numhouses):
            if i != j:
                if checkoverlap(houses[i], houses[j], checkdistance(houses[i], houses[j])):
                    print "There is overlap at the end"



run = run(20)