import sys
 
import pygame
from pygame.locals import *
from spritesheet import *
from item import *
from map import *


class Player():
    def __init__(self, spritesheet:Spritesheet, screen, map:Map):
        #Position & misc
        self.x = 1
        self.y = 1
        self.health = 100

        #Screen to draw to
        self.screen = screen

        #Spritesheet
        self.spritesheet = spritesheet

        #Cordinates for tile on spritesheet
        self.tileCordinate_x = 7
        self.tileCordinate_y = 5

        #gravestone tile x16, y21
        self.map = map

        self.inventory = []
    

    #------------
    #Update logic
    #------------
    def update(self):
        
        #Check if player is dead
        if self.health <= 0:
            self.tileCordinate_x = 16
            self.tileCordinate_y = 21
    
    #-------------------
    #Player draws itself
    #-------------------
    def draw(self):
        self.map.drawEntity(self.x,self.y, (self.tileCordinate_x,self.tileCordinate_y),self)

    #--------------------------------
    #Player handles its own inventory
    #--------------------------------
    def add_item_to_inventory(self,item:Item):
        self.inventory.append(item)

    #-----------------------------------------
    #Check for loot at current player position. if there is loot add it to player inventory and remove from map
    #Adding boolean return to know if there was loot
    #-----------------------------------------
    def check_for_loot(self):
        item = self.map.get_item(self.x,self.y)
        if item != None:
            self.add_item_to_inventory(item)
            self.map.remove_item(item)
            return True, item
        return False, None
    

    #--------------------------
    #Handle entity interraction
    #--------------------------
    def interract_entity(self, x,y):
        entity = self.map.getEntity(x,y)
        if entity !=None:
            
            #Is a door?
            if type(entity) == Door:
                #Is door locked?
                if entity.locked == True:
                    #Check inventory for a key
                    for item in self.inventory:
                        if item.name == "Key":
                            isOpened = entity.unlock(item)
                            if isOpened:
                                self.inventory.remove(item)
                                return "Door-unlocked"
                            else:
                                return "Door-locked"
                    return "Door is locked"
