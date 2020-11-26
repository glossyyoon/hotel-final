import math

def get_distance(a, b):
    return math.sqrt(
        math.pow(a.x - b.x, 2) +
        math.pow(a.y - b.y, 2) +
        math.pow(a.z - b.z, 2)) ** 2

def convert_to_coordinate(raw_position):
    return Coordinate(int(raw_position.split(',')[0]), int(raw_position.split(',')[1]), int(raw_position.split(',')[2]))

class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

place_coord = {}
FLOOR_COUNT = 30
ROOM_COUNT = 10
ROOM_WIDTH = 100
ROOM_MARGIN = 10
HALLWAY_WIDTH = 50
FLOOR_HEIGHT = 120
for floor in range(2, FLOOR_COUNT):
    for room in range(1, ROOM_COUNT):
        place_coord["R" + str(floor) + ("0" if room < 10 else "") + str(room)] = \
        Coordinate(
            (ROOM_WIDTH + ROOM_MARGIN) * room - (ROOM_WIDTH * 10 if room > 5 else 0),
            HALLWAY_WIDTH if room > 5 else 0,
            FLOOR_HEIGHT * floor)
PARK_FLOOR_COUNT = 10
for floor in range(-PARK_FLOOR_COUNT, -1):
    place_coord["P" + ("0" if room < 10 else "") + str(-floor)] = \
        Coordinate(0, 0, FLOOR_HEIGHT * floor)
place_coord["Front"] = Coordinate(250, 50, 0)
place_coord["Kitchen"] = Coordinate(400, 200, 0)
place_coord["Purchasing"] = Coordinate(0, 400, 0)
place_coord["Center"] = Coordinate(700, 800, 0)

def get_place_coord(place):
    return place_coord[place]