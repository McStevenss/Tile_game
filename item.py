import sys
 
import pygame
from pygame.locals import *
from spritesheet import *

class Item():
    def __init__(self, x,y, name="Item", tileX = 18, tileY = 13):
        
 
        #Item variables
        self.name = name
        self.x = x
        self.y = y
        self.description = "an item"

        #Graphics
        self.tileX = tileX
        self.tileY = tileY

        def use(self):
            pass


class Door():
    def __init__(self,x,y):

        #Graphics
        self.x = x
        self.y = y
        self.tileX = 4
        self.tileY = 21

        #Variables
        self.description = "a door"
        self.locked = True


    def unlock(self, key:Item):
        if key.name == "Key":
            #Unlock door and switch sprite to open door
            self.locked = False
            self.tileX = 3
            return True
        return False

