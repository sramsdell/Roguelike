import sys
from objects import Map, Game
from rogue import game
from map_generator import generate_map

sys.dont_write_bytecode = True

grid = Map(generate_map(30, 30), game, 30, 30)

grid1 = Map(["xxxxxxxxxx",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "xxxxxxxxxx"], game)



    
def change_level(game):
    level = game.get_level()
    if level == 1:
        return grid
    if level == 2:
        return grid1
