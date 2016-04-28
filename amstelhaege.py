import random
import math


class House(object):
    def __init__(self, width, length, free):
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

    def checkoverlap(self, house, checkedhouse, distance):
        if distance < house.free or distance < checkedhouse.free:
            return True
        else:
            return False

    def checkdistance(self, house, housechecked, numhouses):
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

        print "distance = ", distance
        if self.checkoverlap(house, housechecked, distance):
            print "There is an overlap with this house"
        return distance


def placehouses(numhouses):
    houses = []
    i = 0
    while i < (numhouses * 0.6):
        houses.append(House(8, 8, 2))
        i += 1
    while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
        houses.append(House(10, 7.5, 3))
        i += 1
    while i >= (numhouses * 0.85) and i < numhouses:
        houses.append(House(11, 10.5, 6))
        i += 1
    return houses


# def replacehouse(house, houses, numhouses):
  #      tempposition = house.position
   #     house.position = map.getrandom(house.width, house.length, house.free)
    #    print "position of house = ", house.position
    #    for i in numhouses:
            # distance = house.map.checkdistance(house, houses[i], numhouses)
        #   if (checkoverlap(house, houses, distance):
      #      houses[i].position = tempposition
      #      break
       # print houses[i].position


def run(numhouses):

    houses = placehouses(numhouses)
    for i in range(numhouses):
        for j in range(numhouses):
            if i == j:
                continue
            houses[i].map.checkdistance(houses[i], houses[j], numhouses)
    # replacehouseh(houses)

run = run(10)