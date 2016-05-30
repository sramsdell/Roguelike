import random

class Room():
    def __init__(self,idenity, h_max, w_max, h_min = 4, w_min = 4):
        self._width = random.randrange(w_min, w_max + 1)
        self._height = random.randrange(h_min, h_max + 1)
        self._idenity = idenity

        self._grid = [["." for col in range(self._width)] for row in range(self._height)]
        self._grid = par(self._grid, self._width, self._height)
    def get_dimentions(self):
        return [self._width, self._height]
    def get_idenity(self):
        return self._idenity
    def get_grid(self):
        return self._grid

def par(grid,x,y):
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
    no_moves = ["x","p"]
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

def main():
        
    value_x = 30
    value_y = 30

    grid = [[" " for col in range(value_x)] for row in range(value_y)]
    grid = par(grid,value_x,value_y)

    rooms = set()
    counter = 0
    while len(rooms) < 20:
        counter += 1
        room = Room(counter, 17, 17)
        rooms.add(room)
    rooms = list(rooms)

    count = 0
    room_count = 0
    while count != 300 or room_count == len(rooms):
        room = random.choice(rooms)
        print room
        offset = grid_offset(value_x, value_y, grid, room)

        flag = True
        no_move = ["x","p","."]
        for i, v in enumerate(room.get_grid()):
            for j, w in enumerate(v):
                try:
                    if grid[i + offset[0]][j + offset[1]] in no_move:
                        flag = False
                except:
                    flag = False
        if flag:
            grid = generate_room(grid,room,offset)
            room_count += 1
         
        count += 1

                    
                
                    
                    

    
    print ""
    print room_count
    for i in grid:
        print " ".join(i)

if __name__ == "__main__":
    main()


