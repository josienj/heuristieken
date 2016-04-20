import random

class House(object):
    def __init__(self, width, length, free):
        self.width = width
        self.length = length
        self.free = free
        self.map = Map()
        self.position = map.getRandom(self.width, self.length, self.free)
        self.pos_X = self.position[0]
        self.pos_Y = self.position[1]

class Position(object):
    def __init__(self, width, length, map):
        position = map.getRandom(width, length)

class Map(object):
    def __init__(self):
        self.x_axis = 150
        self.y_axis = 160

    def getRandom(self, width, length, free):
        x = random.uniform((0 + free), (self.x_axis - (width + free)))
        y = random.uniform((0 + free), (self.y_axis - (length + free)))
        return (x, y)

def run(numhouses):

    house = []
    for i in range(numhouses):
        while i < (numhouses * 0.6):
            house[i].append(House(8, 8, 2))
        while i >= (numhouses * 0.6) and i < (numhouses * 0.85):
            house[i].append(House(10, 7.5, 3))
        while i >= (numhouses * 0.85):
            house[i].append(House(11, 10.5, 6))










