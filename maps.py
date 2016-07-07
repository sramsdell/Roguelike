import sys
from objects import Map, Game
from rogue import game
from map_generator import generate_map

sys.dont_write_bytecode = True

grid = Map(["xxxxxxxxxx",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "xxxxxxxxxx"], game, door_up=False)

grid_post = [Map(generate_map(30, 30), game, 30, 30) for i in range(10)]
grid_pre = ["maybe a warp?", grid]
grids = grid_pre + grid_post

def change_level(game):
    level = game.get_level()
    return grids[level]
