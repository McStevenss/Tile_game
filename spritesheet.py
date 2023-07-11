import sys
 
import pygame
from pygame.locals import *



class Spritesheet():
    def __init__(self, spritesheet,screen):
        self.tilesize = 32
        self.screen = screen
    
        self.spritesheet = pygame.image.load(spritesheet)
    
    
    def image_at(self, x, y):
        """Load a specific image from a specific rectangle."""
        # Load image from x, y, x + offset, y + offset.
        rect = pygame.Rect(x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.spritesheet, (0, 0), rect)
        return image
    

    def get_ammount_of_tiles(self):
        x_tiles = self.spritesheet.get_width() // self.tilesize
        y_tiles = self.spritesheet.get_height() // self.tilesize

        return x_tiles, y_tiles