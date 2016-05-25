import math
import os
import os.path
import csv
import random
import time


# Import parameters from Patameters.py
from Parameters import *


#####
# This function is used to start the simulation
# It will place the waterbodies and houses on the map.
# When everything is placed correctly, it will try to replace houses to increase the maps value.
# While and after running it will save important information to new files.
#####
def run(numhouses, numwaters, runs, attempts, checked):

    # Start the timer by saving the current time to start
    start = time.time()

    # Find existing outputrun.csv files and set counter to last csvrun file + 1
    csvrun = 0
    while os.path.exists("CSVRUN\outputruntommie%s.csv" % csvrun):
        csvrun += 1

    # Set background of the pygame screen to green and update
    screen.fill(GREEN)
    pygame.display.update()

    # Create an object map that is used to store information about what happens in the simulation
    mapinfo = Map()

    # Create an empty list houses
    waters = []

    # While the list of waterbodies is empty, try to place all waterbodies on the map.
    while len(waters) == 0:
        # Try to place all waterbodies on the map.
        waters = placewater(numwaters, mapinfo, screen)

    # Create an empty list houses.
    houses = []

    # While the list of houses is empty, try to place all houses on the map.
    while len(houses) == 0:
        # Set background of the pygame screen to green, draw all waterbodies and update
        screen.fill(GREEN)
        for i in range(numwaters):
            pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
        pygame.display.update()
        # Try to place all houses on the map.
        houses = placehouses(numhouses, waters)

    # Check if houses are placed correctly. If not, place houses again
    for i in range(numhouses):
        if checkoverlap(houses[i], waters, i, False):
            houses = placehouses(numhouses, waters)
        else:
            continue

    # Print waters and houses on the pygame screen and update screen
    for i in range(numwaters):
        pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
    pygame.display.update()
    for i in range(numhouses):
        pygame.draw.rect(screen, houses[i].color, houses[i].rect, 0)
    pygame.display.update()

    # Open/create a new csv file and set a writer
    with open('CSVRUN\outputruntommie%s.csv' % csvrun, "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        # Write to csv the values that will be written to csv file for every run
        writer.writerow(["runs", "totalvalue/-distance"])

        # For all runs, draw the waterbodies, try to replace all houses and draw the houses.
        for j in range(runs):

            # Draw all waterbodies.
            for i in range(numwaters):
                pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)

            # Try to replace all houses and print them to the pygame screen.
            for k in range(numhouses):
                # Draw a green rectangle over the old position of the house.
                pygame.draw.rect(screen, GREEN, houses[k].rect, 0)
                # try to get a new position for the house.
                houses = replacehouse(houses[k], houses, numhouses, k, waters, checked)
                # Get the new (or old) coordinates of the house and draw it to the pygame screen.
                getcoordinates(houses[k])
                houses[k].rect = (houses[k].pos_x_l * PAR, houses[k].pos_y_l * PAR,
                                  houses[k].width * PAR, houses[k].length * PAR)
                pygame.draw.rect(screen, houses[k].color, houses[k].rect, 0)
                pygame.display.update()

            # Calculate the total value of the map.
            if checked:
                totalvalue = calculatevalue(houses, numhouses)
            else:
                totalvalue = calculatedistance(houses, numhouses)

            # Write a new row to the csv file with the current run and totalvalue.
            writer.writerow(["run %s" % j, totalvalue])

            # Print the attempt, the run and the totalvalue of the current run.
            print attempts, "run", j, "= ", totalvalue

    # After all runs, close csv file
    csvfile.close()

    # Print the whole screen from scratch, using the current list waters and houses
    screen.fill(GREEN)
    for i in range(numwaters):
        pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
    for i in range(numhouses):
        pygame.draw.rect(screen, houses[i].color, houses[i].rect, 0)
    pygame.display.update()

    # Calculate totalvalue and totaldistance of the map
    totalvalue = calculatevalue(houses, numhouses)
    totaldistance = calculatedistance(houses, numhouses)

    # End the timer by saving the current time to end
    end = time.time()
    # Calculate the total amount of time that has passed since the beginning of the simulation
    totaltime = end - start

    # Write all essential parameters and results to csv files and image file
    save(numhouses, numwaters, houses, waters, runs, checked, totalvalue, totaldistance, screen, csvrun, totaltime)


#####
# A Class in which the values of the house are first created and stored.
# The values 'basevalue', 'perc' and 'color' are different for each house type.
# These values are added seperately, later in placeHouses.
#####
class House(object):

    def __init__(self, width, length, free):

        # Initialize variables which will be set to actual values in placehouses. These will vary per housetype.
        self.basevalue = 0
        self.perc = 0.00
        self.color = GREEN

        # Declare variables with values given in placehouses. These will vary per housetype.
        self.width = width
        self.length = length
        self.free = free

        # Create a mapobject
        self.map = Map()
        # Use function getrandom to get a random valid position on the map
        self.position = self.map.getrandom(self.width, self.length, self.free)

        # Initialize coordinate-variables which will be assigned in getcoordinates with the current position
        self.pos_x_l = 0
        self.pos_x_r = 0
        self.pos_y_l = 0
        self.pos_y_u = 0
        getcoordinates(self)

        # Create a rect object which is used for printing result on the pygame screen
        self.rect = (self.pos_x_l * PAR, self.pos_y_l * PAR,
                     self.width * PAR, self.length * PAR)


#####
# A Class in which the values of the waterbodies are first created and stored.
# Information about the needed surface of water and the amound of waterbodies
# is given by a mapobject that is made in def run and passed by placewaters
#####
class Water(object):

    def __init__(self, mapwater):

        # Set color of water to blue
        self.color = BLUE

        # Set the needed amount of free distance to 0
        self.free = 0

        # If there is more than 1 waterbodies that has to be made,
        # the surface of the waterbody is a random number between 0 and the remaining surface.
        if mapwater.waterbodies < (NUM_WATER - 1):
            self.surface = random.uniform(0, mapwater.remainingsurface)
            while self.surface == 0 or self.surface == mapwater.remainingsurface:
                self.surface = random.uniform(0, mapwater.remainingsurface)
        # If there is only one waterbody left to place, the waterbody gets all the remaining surface.
        else:
            self.surface = mapwater.remainingsurface
        # Update the remaining surface and waterbodies placed after placing this waterbody.
        mapwater.remainingsurface -= self.surface
        mapwater.waterbodies += 1

        # Use a random 0 or 1 to determine of the width or the length of the waterbody will be bigger.
        rand = random.randint(0, 1)

        # The proportions of the waterbody must be between 1:1 and 1:4
        # If width is bigger, width is between squareroot and 2 times the squareroot of the total surface
        # Length is total surface / width
        if rand == 0:
            self.width = random.uniform(math.sqrt(self.surface), (2 * math.sqrt(self.surface)))
            self.length = self.surface / self.width
        # If length is bigger, width is between squareroot and 2 times the squareroot of the total surface
        # Width is total surface / length
        if rand == 1:
            self.length = random.uniform(math.sqrt(self.surface), (2 * math.sqrt(self.surface)))
            self.width = self.surface / self.length

        # Initialize coordinate-variables which will be assigned in getcoordinates with the current position
        self.position = mapwater.getrandom(self.width, self.length, 0)
        self.pos_x_l = 0
        self.pos_x_r = 0
        self.pos_y_l = 0
        self.pos_y_u = 0
        getcoordinateswater(self)

        # Create a rect object which is used for printing result on the pygame screen
        self.rect = ((self.pos_x_l * PAR), (self.pos_y_l * PAR),
                     (self.width * PAR), (self.length * PAR))


#####
# A Class in which the values of the map are first created and stored.
# Information about the needed map is given in Parameters
#####
class Map(object):

    def __init__(self):

        # Set the x and y range of the map
        self.x_axis = MAP_X
        self.y_axis = MAP_Y

        # Set parameters and variables needed for the waterbodies
        self.totalwater = (MAP_X * MAP_Y) * 0.2
        self.waterbodies = 0
        self.remainingsurface = self.totalwater

    # Get a random x and y coordinate on the map
    def getrandom(self, width, length, free):
        x = random.uniform((0 + free), (self.x_axis - (width + free)))
        y = random.uniform((0 + free), (self.y_axis - (length + free)))

        # Return position x, y
        return x, y


#####
# Get the coordinates of the house, used for calculations
#####
def getcoordinates(house):
    # pos_x_l is the x coordinate of house.position
    house.pos_x_l = house.position[0]
    # pos_x_r is the x coordinate of house.position plus the width of the house
    house.pos_x_r = house.position[0] + house.width
    # pos_y_l is the y coordinate of house.position
    house.pos_y_l = house.position[1]
    # pos_y_u is the y coordinate of house.position plus the length of the house
    house.pos_y_u = house.position[1] + house.length


#####
# Get the coordinates of the waterbody, used for calculations
#####
def getcoordinateswater(water):
    # pos_x_l is the x coordinate of water.position
    water.pos_x_l = water.position[0]
    # pos_x_r is the x coordinate of water.position plus the width of the water
    water.pos_x_r = water.position[0] + water.width
    # pos_y_l is the y coordinate of water.position
    water.pos_y_l = water.position[1]
    # pos_y_u is the y coordinate of water.position plus the length of the waterbody
    water.pos_y_u = water.position[1] + water.length


#####
# This function calculates what the minimal distance of a house is to another object.
# This object may either be another house, or the edge of a map.
#####
def calculatemin_distance(house, houses, numhouses, housenumber):

    # Set minimal distance to the distance to the left edge of the map.
    min_distance = house.pos_x_l

    # If the house is closer to the right edge of the map, make this distance mindistance.
    if house.map.x_axis - house.pos_x_r < min_distance:
        min_distance = house.map.x_axis - house.pos_x_r

    # If the house is closer to the bottom of the map, make this distance mindistance.
    if house.pos_y_l < min_distance:
        min_distance = house.pos_y_l

    # If the house is closer to the top of the map, make this distance mindistance.
    if house.map.y_axis - house.pos_y_u < min_distance:
        min_distance = house.map.y_axis - house.pos_y_u

    # Check the distance to all other houses in list houses, except for itself.
    for i in range(numhouses):
        if i == housenumber:
            continue

        # If distance to another house is less than mindistance, make this distance mindistance.
        tempdistance = checkdistance(house, houses[i])
        if tempdistance < min_distance:
            min_distance = tempdistance

    # Return mindistance as the minimal distance of a house to next object or edge
    return min_distance


#####
# Checks if the given object has overlap with items from a given list.
# If checkwithself is True, this means that the object is a part of given list.
# In order to check the list properly, given object should not be compared to itself.
# Therefore, it will skip the list object 'ownnumber', which is itself.
#####
def checkoverlap(objectchecked, listchecked, ownnumber, checkwithself):

    # Create a counter
    counter = 0

    # Check distance for all items in the list, except for itself.
    for i in range(len(listchecked)):
        if checkwithself:
            if i == ownnumber:
                continue

        # Check distance to other object.
        distance = checkdistance(objectchecked, listchecked[i])

        # If the object or the list objects are water, there is only overlap when distance < 0.
        if objectchecked.color == BLUE or listchecked[i].color == BLUE:

            # If overlap is found, return True.
            if distance < 0:
                return True
            # If no overlap is found, increment counter.
            else:
                counter += 1

        # None of the compared objects are water objects.
        else:

            # If overlap is found, return True.
            # Overlaps when distance to house is less than required detachment of the houses.
            if distance < objectchecked.free or distance < listchecked[i].free:
                return True
            # If no overlap is found, increment counter.
            else:
                counter += 1

        # If checked with list which includes itself, counter must reach length of list -1.
        if checkwithself:
            # If counter reaches length of list -1, no overlap has been found with list. Return False.
            if counter == len(listchecked) - 1:
                return False
        # If checked with list that doesn't include itself, counter must reach length of list.
        else:
            # If counter reaches length of list, no overlap has been found with list. Return False.
            if counter == len(listchecked):
                return False


#####
# This function calculates the distance from one object to another.
# The way in which this is calculated depends on where the objects stand, relative to each other.
# Pythagoras is only needed when the houses do not overlap on the x-axis or y-axis.
#####
def checkdistance(house, housechecked):

    # Use the coordinates of the checked objects to determine the variables that are used for calculation.
    # These variables are only needed to make the calculations more readable.
    x1l = house.pos_x_l
    x1r = house.pos_x_r
    y1l = house.pos_y_l
    y1u = house.pos_y_u
    x2l = housechecked.pos_x_l
    x2r = housechecked.pos_x_r
    y2l = housechecked.pos_y_l
    y2u = housechecked.pos_y_u

    # Create variables dx, dy and distance.
    dx = 0
    dy = 0
    distance = 0

    # If house and house[i] overlap on x-axis
    if x2l < x1l < x2r or x2l > x1l and x1r > x2l:
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

    # return the distance
    return distance


#####
# This function places all required houses on a valid location on the map.
# It will append a house to list houses with values that match the housetype.
# If the first random position overlaps with water or other house, try another random position.
#####
def placehouses(numhouses, waters):

    # Create an empty list houses and a counter for the amound of houses.
    houses = []
    i = 0

    # For the first 15% of the houses, create a house of the third housetype.
    while i < (numhouses * PERCTYPE3):
        # Append the house to houses and set the variables of the housetype.
        houses.append(House(B3, L3, HOUSEFREE3))
        houses[i].basevalue = HOUSEVALUE3
        houses[i].perc = HOUSEPERC3
        houses[i].color = HOUSECOLOR3
        # Increment house counter
        i += 1
    # For the next 25% of the houses, create a house of the second housetype.
    while (numhouses * PERCTYPE3) <= i < (numhouses * (PERCTYPE3 + PERCTYPE2)):
        # Append the house to houses and set the variables of the housetype.
        houses.append(House(B2, L2, HOUSEFREE2))
        houses[i].basevalue = HOUSEVALUE2
        houses[i].perc = HOUSEPERC2
        houses[i].color = HOUSECOLOR2
        # Increment house counter
        i += 1
    # For the last 60% of the houses, create a house of the first housetype.
    while (numhouses * (1 - PERCTYPE1)) <= i < numhouses:
        # Append the house to houses and set the variables of the housetype.
        houses.append(House(B1, L1, HOUSEFREE1))
        houses[i].basevalue = HOUSEVALUE1
        houses[i].perc = HOUSEPERC1
        houses[i].color = HOUSECOLOR1
        # Increment house counter.
        i += 1

    # Draws all houses on the pygame screen and updates display.
    for k in range(numhouses):
        pygame.draw.rect(screen, GREEN, houses[k].rect, 0)
        getcoordinates(houses[k])
        houses[k].rect = (houses[k].pos_x_l * PAR, houses[k].pos_y_l * PAR,
                          houses[k].width * PAR, houses[k].length * PAR)
        pygame.draw.rect(screen, houses[k].color, houses[k].rect, 0)
        pygame.display.update()

    # Checks for all houses in list houses if there is overlap with another house or with water.
    for i in range(numhouses):

        # Draws all houses on the pygame screen and updates display
        for k in range(numhouses):
            pygame.draw.rect(screen, GREEN, houses[k].rect, 0)
            getcoordinates(houses[k])
            houses[k].rect = (houses[k].pos_x_l * PAR, houses[k].pos_y_l * PAR,
                              houses[k].width * PAR, houses[k].length * PAR)
            pygame.draw.rect(screen, houses[k].color, houses[k].rect, 0)
            pygame.display.update()

        # Make a counter to keep track of the amound of times a house tries to get a new position.
        replacecounter = 0

        # Tries positions until it finds a position of the house that has no overlap with houses or water.
        while True:

            # If the current house has tried to get a new position for 500 times, return an empty list houses.
            if replacecounter == 500:
                houses = []
                return houses

            # If no overlap is found with houses, check for overlap with water.
            if not checkoverlap(houses[i], houses, i, True):
                # If no overlap is found with water, break from the while loop.
                if not checkoverlap(houses[i], waters, i, False):
                    break
                # If overlap is found with water, get a new position for the house.
                else:
                    # Increment replacecounter.
                    replacecounter += 1
                    houses[i].position = houses[i].map.getrandom(houses[i].width, houses[i].length, houses[i].free)
                    # Get the new coordinates of the house and draw it on the pygame screen.
                    getcoordinates(houses[i])
                    pygame.draw.rect(screen, houses[i].color, houses[i].rect, 0)
                    pygame.display.update()
            # If overlap is found with houses, get a new position for the house.
            else:
                # Increment replacecounter.
                replacecounter += 1
                houses[i].position = houses[i].map.getrandom(houses[i].width, houses[i].length, houses[i].free)
                # Get the new coordinates of the house and draw it on the pygame screen.
                getcoordinates(houses[i])
                pygame.draw.rect(screen, houses[i].color, houses[i].rect, 0)
                pygame.display.update()

    # Draws all houses on the pygame screen and updates display.
    for k in range(len(houses)):
        pygame.draw.rect(screen, GREEN, houses[k].rect, 0)
        getcoordinates(houses[k])
        houses[k].rect = (houses[k].pos_x_l * PAR, houses[k].pos_y_l * PAR,
                          houses[k].width * PAR, houses[k].length * PAR)
        pygame.draw.rect(screen, houses[k].color, houses[k].rect, 0)
        pygame.display.update()

    # Return list houses.
    return houses


#####
# This function places all required waterbodies on a valid location on the map.
# If the first random position overlaps with another waterbody, try another random position.
#####
def placewater(numwater, mapwater, screen):

    # Create an empty list waterbodies and a counter for the amound of waterbodies.
    waters = []
    i = numwater

    # Make a counter to keep track of the amound of times a house tries to get a new position.
    replacecounter = 0

    # While there are still waterbodies needed to be made, append a waterbody to list waters.
    while i > 0:
        waters.append(Water(mapwater))
        # Increment waterbody counter.
        i -= 1

    # Draw all waterbodies on the pygame screen.
    for i in range(numwater):
        pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
    pygame.display.update()

    # Check for all waterbodies if they have overlap with other waterbodies.
    for i in range(numwater):

        # Tries positions until it finds a position of the waterbody that has no overlap other waterbodies.
        while True:

            # If the current waterbody has tried to get a new position for 500 times, return an empty list waters.
            if replacecounter == 500:
                waters = []
                return waters

            else:
                # If overlap is found with another waterbody, get a new position for the waterbody.
                if checkoverlap(waters[i], waters, i, True):

                    # Increment replacecounter
                    replacecounter += 1

                    # Get new position for waterbody
                    waters[i].position = mapwater.getrandom(waters[i].width, waters[i].length, 0)
                    # Get new coordinates and draw on the pygame screen.
                    getcoordinates(waters[i])
                    waters[i].rect = ((waters[i].pos_x_l * PAR), (waters[i].pos_y_l * PAR), (
                        waters[i].width * PAR), (waters[i].length * PAR))
                    screen.fill(GREEN)
                # If no overlap is found with other waterbodies, break from while loop.
                else:
                    break

    # Draw all waterbodies on the pygame screen.
    screen.fill(GREEN)
    for i in range(numwater):
        pygame.draw.rect(screen, waters[i].color, waters[i].rect, 0)
    pygame.display.update()

    # Return list waters
    return waters


#####
# This function tries to replace a house to a better position.
# The house will only replace if the total value of the map increases.
#####
def replacehouse(house, houses, numhouses, housenumber, waters, checked):

    # Save the old location of the house and the old value of the map.
    oldposition = house.position

    # checked is true, save old total value of map; if false, save old total distance of map.
    if checked:
        oldvalue = calculatevalue(houses, numhouses)
    else:
        oldvalue = calculatedistance(houses, numhouses)

    # Find a valid location on the map.
    while True:

        # Set house.position to new random position on the map and get the coordinates.
        house.position = house.map.getrandom(house.width, house.length, 0)
        getcoordinates(house)
        # Create the rect object of the house.
        house.rect = (house.pos_x_l * PAR, house.pos_y_l * PAR, house.width * PAR, house.length * PAR)

        # If no overlap is found with other houses on new position, check for overlap with waterbodies.
        if not checkoverlap(house, houses, housenumber, True):
            # If no overlap has been found with waterbodies, place house in list houses.
            if not checkoverlap(house, waters, housenumber, False):
                houses[housenumber].position = house.position

                # If checked, calculate new total value of map; if false, calculate new total distance of map.
                if checked:
                    # Calculate the totalvalue of the map.
                    totalvalue = calculatevalue(houses, numhouses)
                else:
                    totalvalue = calculatedistance(houses, numhouses)
                # If the new position of the house does not increase the value of the map, return to old position.
                if totalvalue <= oldvalue:
                    houses[housenumber].position = oldposition
                    getcoordinates(house)

                # Get the rect object of the house and break the while loop.
                houses[housenumber].rect = (
                    house.pos_x_l * PAR, house.pos_y_l * PAR, house.width * PAR, house.length * PAR)
                break

    # Return list houses.
    return houses


#####
# This function calculates the sum of all distances all houses have to other houses or the edge of the map.
#####
def calculatedistance(houses, numhouses):

    # Create variable totaldistance.
    totaldistance = 0

    # For all houses, check what the minimal distance to another object or the edge of the map is.
    for i in range(numhouses):
        min_distance = calculatemin_distance(houses[i], houses, numhouses, i)
        # Increment the totaldistance with the found minimal distance.
        totaldistance += min_distance

    # Return the totaldistance
    return totaldistance


#####
# This function calculates the total value of all the houses on the map.
#####
def calculatevalue(houses, numhouses):

    # create variable totalvalue.
    totalvalue = 0

    # Check the value of all houses.
    for i in range(numhouses):
        min_distance = calculatemin_distance(houses[i], houses, numhouses, i) - houses[i].free
        # Increment totalvalue with the value of the current house.
        totalvalue += houses[i].basevalue * (1 + (houses[i].perc * min_distance))

    # Return the totalvalue.
    return totalvalue


#####
# This function prints all important variables to csv files and an image file.
#####
def save(numhouses, numwaters, houses, waters, runs, checked, totalvalue, totaldistance, screen, csvrun, totaltime):

    # Finds existing image files and assures no file is overwritten
    pngcount = 0
    while os.path.exists("Images\outputtommie%s.png" % pngcount):
        pngcount += 1
    # Print visual outcome of run in image file
    outputfinal = os.path.join(SAVE_PATH_PNG, 'outputtommie' + pngcount.__str__())
    pygame.image.save(screen, outputfinal + '.png')

    # Finds existing csv files and assures no file is overwritten
    csvcount = 0
    while os.path.exists("CSV\outputtommie%s.csv" % csvcount):
        csvcount += 1
    # Print details of outcome of run in csv file
    with open("CSV\outputtommie%s.csv" % csvcount, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["numhouses", "runs", "totalvalue", "totaldistance"])
        writer.writerow([numhouses, runs, totalvalue, totaldistance])
        writer.writerow(["\n"])

        # Print details of waterbodies
        writer.writerow(["water", "position", "width", "length"])
        for i in range(numwaters):
            writer.writerow(["water" + i.__str__(), waters[i].position, waters[i].width, waters[i].length])
        writer.writerow(["\n"])

        # Print details of houses
        writer.writerow(["house", "position", "width", "length", "free"])
        for j in range(numhouses):
            writer.writerow(["house" + j.__str__(), houses[j].position, houses[j].width, houses[j].length,
                            houses[j].free])

    # Close csv file.
    csvfile.close()

    # Print results of run in total.csv
    with open('total.csv', "a") as writefile:
        writer = csv.writer(writefile, delimiter=',', lineterminator='\n')
        writer.writerow(
            [numhouses, numwaters, runs, checked, totalvalue, totaldistance, "outputtommie%s.csv" % csvcount,
                "outputruntommie%s.csv" % csvrun, "output%s.png" % pngcount, totaltime])

    # Close csv file.
    writefile.close()


#####
# This code is used to start the run function.
# The number of tries, runs and number of houses are given in Parameters.py
# Each try will start with a required number of waterbodies, ranging from 1 to 4.
#####
i = 0
j = 0
k = 0
TRY = 0
while i < NUM_TRY20:
    NUM_WATER = random.randint(1, 4)
    run(NUM_HOUSES20, NUM_WATER, RUNS20, TRY, CHECKED)
    i += 1
    TRY += 1
while j < NUM_TRY40:
    NUM_WATER = random.randint(1, 4)
    run(NUM_HOUSES40, NUM_WATER, RUNS40, TRY, CHECKED)
    j += 1
    TRY += 1
while k < NUM_TRY60:
    NUM_WATER = random.randint(1, 4)
    run(NUM_HOUSES60, NUM_WATER, RUNS60, TRY, CHECKED)
    k += 1
    TRY += 1