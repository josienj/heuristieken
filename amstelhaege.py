import random
import math

class House(object):
    def __init__(self, width, length, free):
        self.width = width
        self.length = length
        self.free = free
        map = Map()
        self.position = map.getRandom(self.width, self.length, self.free)
        self.pos_X_L = self.position[0]
        self.pos_X_R = self.position[0] + width
        self.pos_Y_O = self.position[1]
        self.pos_Y_B = self.position[1] + length


class Position(object):
    def __init__(self, width, length, map):
        position = map.getRandom(width, length)
        print position + "in init in pos"



class Map(object):
    def __init__(self):
        self.x_axis = 150
        self.y_axis = 160

    def getRandom(self, width, length, free):
        x = random.uniform((0 + free), (self.x_axis - (width + free)))
        y = random.uniform((0 + free), (self.y_axis - (length + free)))
        print "(x, y) in getRandom = ", (x, y)
        return (x, y)

    #def checkOverlap(self, house, houses, numhouses):


    def checkDistance(self, house, houses, numhouses):
        for i in range(numhouses):
            if house.pos_X_L == houses[i].pos_X_L:
                continue

            if houses[i].pos_X_L > house.pos_X_L:
                if houses[i].pos_X_L < house.pos_X_R:
                    if house.pos_Y_O < houses[i].pos_Y_O:
                        distance = houses[i].pos_Y_O - house.pos_Y_B
                        print "house-i boven house"
                    else:
                        distance = houses[i].pos_Y_B - house.pos_Y_O
                        print "house-i onder house"
                elif houses[i].pos_Y_O > house.pos_Y_O:
                    dY = houses[i].pos_Y_O - house.pos_Y_B
                    dX = houses[i].pos_X_L - house.pos_X_R
                    distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))
                    print "house-i rechts boven house"
                elif houses[i].pos_Y_O < house.pos_Y_O:
                    dY = house.pos_Y_O - houses[i].pos_Y_B
                    dX = houses[i].pos_X_L - house.pos_X_R
                    distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))
                    print "house-i rechts onder house"
            if houses[i].pos_X_L < house.pos_X_L:
                if houses[i].pos_X_R > house.pos_X_L:
                    if house.pos_Y_O < houses[i].pos_Y_O:
                        distance = houses[i].pos_Y_O - house.pos_Y_B
                        print "house-i boven house"
                    else:
                        distance = houses[i].pos_Y_B - house.pos_Y_O
                        print "house-i onder house"
                elif houses[i].pos_Y_O > house.pos_Y_O:
                    dY = houses[i].pos_Y_O - house.pos_Y_B
                    dX = house.pos_X_L - houses[i].pos_X_R
                    distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))
                    print "house-i links boven house"
                elif houses[i].pos_Y_O < house.pos_Y_O:
                    dY = house.pos_Y_O - houses[i].pos_Y_B
                    dX = house.pos_X_L - houses[i].pos_X_R
                    distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))
                    print "house-i links onder house"

            print distance


def placeHouses(numhouses):

    houses = []
    i = 0
    while i < (numhouses * 0.6):
        print i, "in 1st while"
        houses.append(House(8, 8, 2))
        print "position in run = ", houses[i].position, '\n'
        i += 1
    while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
        print i, "in 2nd while"
        houses.append(House(10, 7.5, 3))
        print "position in run = ", houses[i].position, '\n'
        i += 1
    while i >= (numhouses * 0.85) and i < numhouses:
        print i, "in 3rd while"
        houses.append(House(11, 10.5, 6))
        print "position in run = ", houses[i].position, '\n'
        i += 1
    return houses



#def replaceHouses(houses):
 #   for i in range(20):
  #      tempposition = houses[i].position
   #     houses[i].position = map.getRandom(houses[i].width, houses[i].length, houses[i].free)
    #    print houses[i].position
     #   if (replaceHouses(house[i], houses):
      #      houses[i].position = tempposition
       # print houses[i].position



def run(numhouses):

    map = Map()
    houses = placeHouses(numhouses)
    map.checkDistance(houses[0], houses, numhouses)
    #replaceHouses(houses)

run = run(2)