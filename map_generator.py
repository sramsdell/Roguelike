import sys
sys.dont_write_bytecode = True
import random
import math
import copy

def distance(x, y):
    """ takes lists """
    return math.sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))


class Room():
    def __init__(self, idenity, h_max, w_max, h_min=5, w_min=5):
        self._width = random.randrange(w_min, w_max + 1)
        self._height = random.randrange(h_min, h_max + 1)
        self._idenity = idenity
        self._center = [self._height // 2, self._width // 2]
        self._grid = [["." for col in range(self._width)]
                      for row in range(self._height)]
        self._grid = par(self._grid, self._width, self._height)
        self._center_in_map = [0, 0]
        self._connect = False

    def get_dimentions(self):
        return [self._width, self._height]

    def get_idenity(self):
        return self._idenity

    def get_grid(self):
        return self._grid

    def get_center(self):
        return self._center

    def set_cim(self, cim):
        self._center_in_map = cim

    def get_cim(self):
        return self._center_in_map

    def set_connect(self, boo):
        self._connect = True

    def get_connect(self):
        return self._connect


def par(grid, x, y):
    value_x = x
    value_y = y
    for i, v in enumerate(grid):
        for j, w in enumerate(v):

            if j == value_x - 1 or i == value_y - 1 or i == 0 or j == 0:
                grid[i][j] = "x"
    return grid


def grid_offset(value_x, value_y, grid, room):

    grid_ran_x = random.randrange(value_x)
    grid_ran_y = random.randrange(value_y)
    no_moves = ["x", "p"]
    while True:
        if grid[grid_ran_x][grid_ran_y] not in no_moves:
            return [grid_ran_x, grid_ran_y]
        else:
            grid_ran_x = random.randrange(value_x)
            grid_ran_y = random.randrange(value_y)


def generate_room(grid, room, offset):
    new_grid = grid[:][:]
    for i, v in enumerate(room.get_grid()):
        for j, w in enumerate(v):
            new_grid[i + offset[0]][j + offset[1]] = room.get_grid()[i][j]
    return new_grid


def generate_map(x, y):

    value_x = x
    value_y = y

    grid = [[" " for col in range(value_x)] for row in range(value_y)]
    grid = par(grid, value_x, value_y)

    rooms = set()
    counter = 0
    while len(rooms) < 100:
        counter += 1
        room = Room(counter, 17, 17)
        rooms.add(room)
    rooms = list(rooms)

    count = 0
    room_count = 0
    final_rooms = []
    while count != 300:
        room = random.choice(rooms)

        offset = grid_offset(value_x, value_y, grid, room)

        flag = True
        no_move = ["x", "p", "."]
        for i, v in enumerate(room.get_grid()):
            for j, w in enumerate(v):
                try:
                    if grid[i + offset[0]][j + offset[1]] in no_move:
                        flag = False
                except:
                    flag = False

        if flag:

            grid = generate_room(grid, room, offset)
            room_count += 1
            room.set_cim([offset[1] + room.get_center()[1],
                          offset[0] + room.get_center()[0]])

            """ I'm using this deepcopy because I somehow ran
                into a alias problem with the room class, which I have no
                idea how is possible at this time. remember to ask someone
                smarter than myself at some point after clean code a bit"""
            acopy = copy.deepcopy(room)
            final_rooms.append(acopy)

        count += 1

    final_rooms_sorted = []

    for i, room in enumerate(final_rooms):
        big_magic_number = float("INF")
        for j, w in enumerate(final_rooms):

            if w not in final_rooms_sorted:
                if j == 0:
                    final_rooms_sorted.append(w)
                    continue
                else:
                    temp = distance(final_rooms[i - 1].get_cim(), w.get_cim())
                    if temp < big_magic_number:
                        big_magic_number = temp
                final_rooms_sorted.insert(i-1, w)
                w.set_connect(True)

    for ind, room in enumerate(final_rooms_sorted):
        if ind + 1 == len(final_rooms_sorted):
            break
        start = room.get_cim()
        end = final_rooms_sorted[ind + 1].get_cim()

        while start[1] != end[1]:
            if start[1] >= end[1]:
                grid[start[1]][start[0]] = "."
                start[1] -= 1
            else:
                grid[start[1]][start[0]] = "."
                start[1] += 1

        while start[0] != end[0]:
            if start[0] >= end[0]:
                grid[start[1]][start[0]] = "."
                start[0] -= 1
            else:
                grid[start[1]][start[0]] = "."
                start[0] += 1

    return grid
