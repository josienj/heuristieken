def replacehouse(house, houses, numhouses, runs, housenumber, runinfo):
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
    houses[housenumber].rect = ((house.pos_x_l * PAR), (house.pos_y_l * PAR),
                                (house.width * PAR), (house.length * PAR))
    return houses
