from objects import Map, Game
from rogue import game
from map_generator import generate_map

grid = Map(generate_map(60, 60), game, 60, 60)

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
