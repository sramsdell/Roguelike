from objects import Map, Game
from rogue import game
from map_generator import generate_map

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
