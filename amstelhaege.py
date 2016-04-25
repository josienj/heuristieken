import random

#
class House(object):
    def __init__(self, width, length, free):
        self.width = width
        self.length = length
        self.free = free
        map = Map()
        self.position = map.getRandom(self.width, self.length, self.free)
        self.pos_X = self.position[0]
        print self.position[0]
        self.pos_Y = self.position[1]
        print self.position[1]

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
        print (x, y)
        return (x, y)

def run(numhouses):

    house = []
    print house
    i = 0
    for i in range(numhouses):
        while i < (numhouses * 0.6):
            house.append(House(8, 8, 2))
            house[i].position
            print i, "in 1st while"
            i += 1
        while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
            house.append(House(10, 7.5, 3))
            house[i].position
            print i, "in 2nd while"
            i += 1
        while i >= (numhouses * 0.85) and i < numhouses:
            house.append(House(11, 10.5, 6))
            house[i].position
            print i, "in 3rd while"
            i += 1

    return house

run = run(20)