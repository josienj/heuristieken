import random

class House(object):
    def __init__(self, width, length, free):
        self.width = width
        self.length = length
        self.free = free
        map = Map()
        self.position = map.getRandom(self.width, self.length, self.free)
        self.pos_X = self.position[0]
        print "X in House = ", self.position[0]
        self.pos_Y = self.position[1]
        print "Y in House = ", self.position[1]

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

def placeHouses(numhouses):

    houses = []
    print houses
    i = 0
    while i < (numhouses * 0.6):
        print i, "in 1st while"
        houses.append(House(8, 8, 2))
        print "position in run = ", houses[i].position
        i += 1
    while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
        print i, "in 2nd while"
        houses.append(House(10, 7.5, 3))
        print "position in run = ", houses[i].position
        i += 1
    while i >= (numhouses * 0.85) and i < numhouses:
        print i, "in 3rd while"
        houses.append(House(11, 10.5, 6))
        print "position in run = ", houses[i].position
        i += 1
    return houses

def run(numhouses):

    print "before placement"
    houses = placeHouses(numhouses)
    print houses
    print "after placement"

run = run(20)