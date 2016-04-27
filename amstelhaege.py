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
        print "(x, y) = ", x, y
        return x, y


    def checkOverlap(self, house, houses, numhouses):
    # if (overlap):
        # return True
    # else:
        return False


    def checkdistance(self, house, houses, numhouses):
        for i in range(numhouses):
            if house.pos_X_L == houses[i].pos_X_L:
                continue

            # If house and house[i] overlap on x-axis
            elif (house.pos_X_L > houses[i].pos_X_L and house.pos_X_L < houses[i].pos_X_R
                or houses[i].pos_X_L > house.pos_X_L and houses[i].pos_X_L < house.pos_X_R):
                # If house is lower than house[i]
                if house.pos_Y_O < houses[i].pos_Y_O:
                    distance = houses[i].pos_Y_O - house.pos_Y_B
                # If house is higher than house[i]
                elif house.pos_Y_O > houses[i].pos_Y_O:
                    distance = house.pos_Y_O - houses[i].pos_Y_B

            # If house and house[i] overlap on y-axis
            elif (house.pos_Y_O > houses[i].pos_Y_O and house.pos_Y_O < houses[i].pos_Y_B
                  or houses[i].pos_Y_O > house.pos_Y_O and houses[i].pos_Y_O < house.pos_Y_B):
                # If house is lower than house[i]
                if house.pos_X_L > houses[i].pos_X_L:
                    distance = house.pos_X_L - houses[i].pos_X_R
                # If house is higher than house[i]
                elif house.pos_X_L < houses[i].pos_X_L:
                    distance = houses[i].pos_X_L - house.pos_X_R

            # If house is left of house[i]
            elif houses[i].pos_X_L > house.pos_X_L and houses[i].pos_X_L >= house.pos_X_R:
                # If house is lower than house[i]
                if houses[i].pos_Y_O > house.pos_Y_O:
                    dY = houses[i].pos_Y_O - house.pos_Y_B
                    dX = houses[i].pos_X_L - house.pos_X_R
                    distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))
                # if house is higher than house[i]
                elif houses[i].pos_Y_O < house.pos_Y_O:
                    dY = house.pos_Y_O - houses[i].pos_Y_B
                    dX = houses[i].pos_X_L - house.pos_X_R
                    distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))

            # If house is right of house[i]
            elif houses[i].pos_X_L < house.pos_X_L and houses[i].pos_X_R <= house.pos_X_L:
                # If house is lower than house[i]
                if houses[i].pos_Y_O > house.pos_Y_O:
                    dY = houses[i].pos_Y_O - house.pos_Y_B
                    dX = house.pos_X_L - houses[i].pos_X_R
                    distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))
                # If house is higher than house[i]
                elif houses[i].pos_Y_O < house.pos_Y_O:
                    dY = house.pos_Y_O - houses[i].pos_Y_B
                    dX = house.pos_X_L - houses[i].pos_X_R
                    distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))

            print distance


def placehouses(numhouses):

    houses = []
    i = 0
    while i < (numhouses * 0.6):
        print i, "in 1st while"
        houses.append(House(8, 8, 2))
        i += 1
    while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
        print i, "in 2nd while"
        houses.append(House(10, 7.5, 3))
        i += 1
    while i >= (numhouses * 0.85) and i < numhouses:
        print i, "in 3rd while"
        houses.append(House(11, 10.5, 6))
        i += 1
    return houses


# def replaceHouses(houses):
 #   for i in range(20):
  #      tempposition = houses[i].position
   #     houses[i].position = map.getRandom(houses[i].width, houses[i].length, houses[i].free)
    #    print houses[i].position
     #   if (replaceHouses(house[i], houses):
      #      houses[i].position = tempposition
       # print houses[i].position


def run(numhouses):

    houses = placehouses(numhouses)
    houses[0].map.checkdistance(houses[0], houses, numhouses)
    # replaceHouses(houses)

run = run(20)