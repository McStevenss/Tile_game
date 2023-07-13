import sys
 
import pygame
from pygame.locals import *
from spritesheet import *
import random

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
    
class Loot_Creator():
    def __init__(self):

        self.prefixes = {"Common":(0,45), "Uncommon": (45,65), "Rare":(65,75), "Epic": (75,85), "Legendary":(85,95), "Godly":(95,100)}
        self.postfixes = ["","of Strength", "of Intelligence", "of Dexterity"]

        #loot_type protocol: "name": (x_start,x_end,y), x and y being tile cordinates in the spritesheet
        self.loot_types = {
            "Poleaxe": (1,8,11),
            "Projectile": (0,3,10),
            "Spear": (4,10,10),
            "Dagger": (11,15,10),
            "Scroll": (10,34,17),
            "Sheild": (0,5,12),
            "Ring": (0,13,14),
            "Wand": (0,18,19),
            "Potion": (24,39,16),
            "Armor": (30,32,12),
            "Helmet": (32,35,11),
            "Head Cap": (25,28,11),
            "Cloak": (34,38,12),
            "Necklace": (14,24,14),
            "Gloves": (12,15,13),
            "Shoes": (16,25,13),
            "Diamond": (0,17,20)
            }
        
    #-------------
    #Generate loot
    #-------------
    def get_random_loot(self):

        loot_type = random.choice(list(self.loot_types.items()))
        loot_tile = random.randint(loot_type[1][0],loot_type[1][1])

        loot_rarity = random.randint(0,100)


        item_prefix = ""
        item_postfix = self.postfixes[random.randint(0,len(self.postfixes)-1)]
        for rarity in self.prefixes:
            if loot_rarity > self.prefixes[rarity][0] and loot_rarity < self.prefixes[rarity][1]:
                item_prefix = rarity

        print(f"Generated loot of {item_prefix} quality!")

        name = f"{item_prefix} {loot_type[0]} {item_postfix}"

        return Item(0,0,name,loot_tile,loot_type[1][2])


