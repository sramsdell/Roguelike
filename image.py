import sys
import os
sys.dont_write_bytecode = True
import pygame
    
class ImageInfo:
    def __init__(self, center, size, animated = False,lifespan = None):
        self.center = center
        self.size = size
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


##center, size, radius = 0, animated = False, lifespan = None
blue_potion_info = ImageInfo((25,25),(50,50))
blue_potion_image = pygame.image.load(os.path.join("images","blue_potion.png"))

brick_0 = pygame.image.load(os.path.join("images","Brick_0.png"))
brick_1 = pygame.image.load(os.path.join("images","Brick_1.png"))
brick_2 = pygame.image.load(os.path.join("images","Brick_2.png"))
brick_3 = pygame.image.load(os.path.join("images","Brick_3.png"))

floor_1 = pygame.image.load(os.path.join("images","floor_1.png"))
floor_2 = pygame.image.load(os.path.join("images","floor_2.png"))
floor_3 = pygame.image.load(os.path.join("images","floor_3.png"))
