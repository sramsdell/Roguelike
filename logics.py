import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from hero import *
from mob import *
from tile import *
from item import *
from game_camera import *
from colors import *

def spawn_pos(grid, game):
    lis = []
    for i, v in enumerate(grid.get_map()):
        for j, w in enumerate(v):

            if grid.get_map()[j][i] == ".":
                    lis += [[i * game.get_scale(), j * game.get_scale()]]
    pos = random.choice(lis)
    return pos


def mob_spawn(grid, game):
    pos = spawn_pos(grid, game)
    if len(grid.get_mob_set()) < 10:
        mob = Mob(pos, game)
        grid.add_mob_to_set(mob)


def item_spawn(grid, game):
    pos = spawn_pos(grid, game)
    if len(grid.get_mob_set()) < 4:
        item = Item(pos, game)
        grid.add_item_to_set(item)


def hero_spawn(grid, game):
    pos = spawn_pos(grid, game)
    if len(game.get_hero_set()) < 1:
        hero = Hero(pos, game, bot=False)
        camera = Camera(game, hero)
        game.add_hero_to_set(hero)
        game.add_camera_to_set(camera)
        camera.spawn(hero.get_pos())


def hero_teleport(grid, game):
    pos = spawn_pos(grid, game)
    for camera in game.get_camera_set():
        camera.spawn(pos) 
    for hero in game.get_hero_set():
        hero.tele_pos(pos)   
    
def heros_mob_collide(hero, game, grid):
    mob_set = grid.get_mob_set().copy()
    heros = game.get_hero_set()
    for mob in mob_set:
        for hero in heros:
            if mob.get_pos() == hero.get_pos():
                mob.dead(grid, ".")
                grid.del_mob_from_set(mob)

def heros_door_collide(hero, game, grid):
    tiles = grid.get_tile_set()
    heros = game.get_hero_set()
    for tile in tiles:
        if tile.get_type() == "Door":

            for hero in heros:
                if tile.get_pos() == hero.get_pos():
                    game.add_level()

        if tile.get_type() == "Door_up":

            for hero in heros:
                if tile.get_pos() == hero.get_pos():
                    game.sub_level()

    
def heros_item_collide(hero, game, grid):
    item_set = grid.get_item_set().copy()
    heros = game.get_hero_set()
    for item in item_set:
    	for hero in heros:
            if item.get_pos() == hero.get_pos():
    		hero.add_held_item_to_set(item)
    		grid.del_item_from_set(item)


def tile_generate(game, grid):
    scale = game.get_scale()
    x = 0
    for i, v in enumerate(grid.get_map()):
            for j, w in enumerate(v):
                if w == "x" or w == " ":
                    x += 1
                    if len(grid.get_tile_set()) < x:
                        tile = Wall([j, i], scale)
                        grid.add_tile_to_set(tile)

                if w == "d":
                    x += 1
                    if len(grid.get_tile_set()) < x:
                        tile = Door([j, i], scale)
                        grid.add_tile_to_set(tile)

                if w == "D":
                    x += 1
                    if len(grid.get_tile_set()) < x:
                        tile = Door_up([j, i], scale)
                        grid.add_tile_to_set(tile)

                if w == ".":
                    x += 1
                    if len(grid.get_tile_set()) < x:
                        tile = Floor([j, i], scale)
                        grid.add_tile_to_set(tile)


def logic(game, grid, screen):
    mob_spawn(grid, game)
    tile_generate(game, grid)
    hero_spawn(grid, game)
    item_spawn(grid, game)
    for camera in game.get_camera_set():
        camera.in_view()

        for item in grid.get_item_set():
            item.render(screen, camera)

        for tile in grid.get_tile_set():
            tile.render(screen, camera)

        for mob in grid.get_mob_set():
            mob.hunt(grid, game)
            mob.render(screen, camera)
            mob.map_update(grid, mob.get_value())

        for hero in game.get_hero_set():
            level = game.get_level()
            heros_door_collide(hero, game, grid)
            heros_mob_collide(hero, game, grid)
            heros_item_collide(hero, game, grid)
            hero.render(screen, camera)
            hero.map_update(grid, value=hero.get_value())

            return level
    
def logic_2(game, grid, screen, level):
    for hero in game.get_hero_set():

        if game.get_level() != level:
            hero_teleport(grid, game)
