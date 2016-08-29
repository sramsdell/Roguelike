import sys
sys.dont_write_bytecode = True
import pygame
import random
import copy
from helper import *
from hero import *
from mob import *
from tile import *
from item import *
from game_camera import *
from colors import *
from sub_menu import Message

def mob_spawn(grid, game):
    pos = spawn_pos(grid, game)
    fogs = []
    for fog in grid.get_fog_set():
        fogs.append(fog.get_pos())
    if pos in fogs:
        if len(grid.get_mob_set()) < 1:
            mob = Spider_1(pos, game)
            grid.add_mob_to_set(mob)


def item_spawn(grid, game):
    pos = spawn_pos(grid, game)
    if len(grid.get_item_set()) < 5:
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

def attacks_mob_collide(game, grid):
    mob_set = grid.get_mob_set().copy()
    attacks = game.get_attack_set()
    
    for mob in mob_set:
        for attack in attacks:
            
            if mob.get_pos() == attack.get_pos():
                mob.sub_hp(attack.attack())

        if mob.get_hp() <= 0:
            mob.dead(grid, ".")
            grid.del_mob_from_set(mob)

def attacks_hero_collide(hero, game):
    attacks = game.get_mob_attack_set()
    if True:
        for attack in attacks:
            if hero.get_pos() == attack.get_pos():
                hero.sub_hp(attack.attack())

        if hero.get_hp() <= 0:
            pass

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
    sub_menu = game.get_sub_menu()
    message = game.get_message()

    for tile in tiles:
        if tile.get_type() == "Door":

            for hero in heros:
                
                if game.get_hero_ref() != hero.get_pos():
                    if tile.get_pos() == hero.get_pos():
                        message.selection("door")
                        sub_menu.turn_on()    

                        if sub_menu.get_select():
                            sub_menu.select_off()
                            sub_menu.turn_off()
                            game.add_level()

        if tile.get_type() == "Door_up":

            for hero in heros:
                if tile.get_pos() == hero.get_pos():
                    game.sub_level()

    
def heros_item_collide(hero, game, grid):
    item_set = grid.get_item_set().copy()
    heros = game.get_hero_set()
    sub_menu = game.get_sub_menu()
    message = game.get_message()

    for item in item_set:
    	for hero in heros:

            if game.get_hero_ref() != hero.get_pos():
                if item.get_pos() == hero.get_pos():
                    message.selection("item", item.get_type(),"?")
                    sub_menu.turn_on()
                    if sub_menu.get_select():
                        sub_menu.select_off()
                        sub_menu.turn_off()
                        hero.add_held_item(item)
                        grid.del_item_from_set(item)

def heros_fog_collide(hero, game, grid):
    scale = game.get_scale()
    fogs = grid.get_fog_set().copy()
    heros = game.get_hero_set()
    for fog in fogs:
        for hero in heros:
            sight = hero.get_sight()
            if distance(hero.get_pos(), fog.get_pos()) <= scale * sight:
                pos = [fog.get_pos()[0] / scale, fog.get_pos()[1] / scale]
                grid.alt_fog_grid(pos, 1)
                grid.del_fog_from_set(fog)

def attack_age(game):
    for attack in game.get_attack_set():

        if attack.get_lifespan() < 0:
            game.del_attack_from_set(attack)
            break
    for attack in game.get_mob_attack_set():

        if attack.get_lifespan() < 0:
            game.del_attack_from_set(attack)
            break

def fog_tile_generate(game, grid):
    scale = game.get_scale()
    x = 0
    test = 0
    for i, v in enumerate(grid.get_fog_grid()):
        for j, w in enumerate(v):
            if w == 0:
                x += 1
                if len(grid.get_fog_set()) < x:
                    fog = Fog([j, i], scale)
                    grid.add_fog_to_set(fog)


def hero_die(game, game_grids, state):
    for hero in game.get_hero_set():
        if hero.get_hp() > 0:
            return "2"
        
    self = state
    game_grids.reset()
    game.reset_game(self.grid)
    return "1"


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

def logic(game, grid, screen, state):
    """note to self, I think you figured out why update and render
    should have different hooks"""
    fog_tile_generate(game, grid)
    mob_spawn(grid, game)
    tile_generate(game, grid)
    hero_spawn(grid, game)
    #item_spawn(grid, game)

    for camera in game.get_camera_set():
        camera.in_view()

        for tile in grid.get_tile_set():
            tile.render(screen, camera, grid)
        
        for item in grid.get_item_set():
            item.render(screen, camera, grid)

        for attack in game.get_attack_set():
            attacks_mob_collide(game, grid)

        for mob in grid.get_mob_set():
            mob.hunt(grid, game)
            mob.render(screen, camera, grid)
            mob.map_update(grid, mob.get_value())

        for attack in game.get_attack_set():
            attack.render(screen, camera)

        for fog_tile in grid.get_fog_set():
            fog_tile.render(screen, camera)

        for hero in game.get_hero_set():
            attack_age(game)
            level = game.get_level()
            heros_door_collide(hero, game, grid)
            heros_fog_collide(hero, game, grid)
            heros_mob_collide(hero, game, grid)
            attacks_hero_collide(hero, game)
            heros_item_collide(hero, game, grid)
            hero.render(screen, camera)
            hero.map_update(grid, value=hero.get_value())
            hero.update(grid)
            return level


def logic_2(game, grid, screen, level):
    for hero in game.get_hero_set():

        if game.get_level() != level:
            hero_teleport(grid, game)
