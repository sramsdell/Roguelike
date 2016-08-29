import sys
sys.dont_write_bytecode = True
import pygame
from colors import *
pygame.init()


messages = {"door" : "Go down the door?",
            "item" : "pick up the ",
            "test" : "testesttesttestest"
            }

class Message:
    def __init__(self, size, scale):
        self.size = size
        self.scale = scale
        
        self.menu = pygame.Surface((self.size[0] - self.scale * 6, self.scale * 2))
        #self.menu.set_alpha(64)
        self.menu.fill(BLUE)

        self.font = pygame.font.SysFont("fixedsys", self.scale)

        self._key = "test"
        self._name = ""
        self._que = ""

    def selection(self, key, name="", que=""):
        self._key = key
        self._name = name
        self._que = que
        

    def render(self, screen):
        self.text = self.font.render(messages[self._key],
                                       1,(255,255,255))
        self.text2 = self.font.render(self._name + self._que,
                                       1,(255,255,255))

        screen.blit(self.menu,
                    (self.scale, self.size[1] - self.scale * 2))
            
        screen.blit(self.text,
                    (self.scale, self.size[1] - self.scale * 2))
        screen.blit(self.text2,
                    (self.scale, self.size[1] - self.scale * 1))
        
class SubMenu:

    def __init__(self, size, scale):
        self._on = False
        self.size = size
        self.scale = scale
        self._switch = True
        self._select = False

        self.menu = pygame.Surface((self.scale * 2.25, self.scale * 2))
        #self.menu.set_alpha(64)
        self.menu.fill(BLUE)

        self.font = pygame.font.SysFont("fixedsys", self.scale)
        self.menu1a = self.font.render("Yes",
                                       1,(255,255,255))

        self.menu2a = self.font.render("No",
                                       1,(255,255,255))

        self.menu1b = self.font.render("Yes",
                                       1,RED)

        self.menu2b = self.font.render("No",
                                       1,RED)

    def get_is_on(self):
        return self._on

    def get_select(self):
        return self._select

    def select_off(self):
        self._select = False

    def get_switch(self):
        return self._switch

    def turn_on(self):
        self._on = True

    def turn_off(self):
        self._on = False

    def render(self, screen):
        screen.blit(self.menu,
                    (self.size[0] - self.scale * 4, self.size[1] - self.scale * 3))
        if self._switch:
            screen.blit(self.menu1b,
                        (self.size[0] - self.scale * 4, self.size[1] - self.scale * 3))
            screen.blit(self.menu2a,
                        (self.size[0] - self.scale * 4, self.size[1] - self.scale * 2))
        else:
            screen.blit(self.menu1a,
                        (self.size[0] - self.scale * 4, self.size[1] - self.scale * 3))
            screen.blit(self.menu2b,
                        (self.size[0] - self.scale * 4, self.size[1] - self.scale * 2))

    def event_handler(self, key, game):
        for i in game.get_hero_set():
            hero = i
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            if self._switch:
                self._select = True
                self._on = False
            else:
                self._switch = True
                self._on = False
                game.alt_hero_ref(hero.get_pos())

        if key == pygame.K_UP:
            self._switch = True

        if key == pygame.K_DOWN:
            self._switch = False
