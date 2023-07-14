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

        self.consumable = False
        self.equippable = False
        self.cursed = False
        self.blessed = False

        self.isequipped = False

        #Stat_modifier
        #I dont know what the best way is, right now i think i will pass a list of strings
        #Such as "STR+10" means +10 strength, "DEX+10" adds 10 dexterity and so on... Its also possible for a negative modifier such as "STR-10" 
        #Also if a weapon, it has a base damage: DMG+-N
        
        #Possible modifiers right now:
        #DMG+-N
        #HP+-N
        #STR+-N
        #LVL+-N
        #DEX+-N
        #CON+-N
        #INT+-N
        #WIS+-N
        self.stat_modifier = []

        #Graphics
        self.tileX = tileX
        self.tileY = tileY

    def use(self):
        return self.stat_modifier, self.consumable,self.equippable


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
        self.postfixes = ["","of Strength", "of Intelligence", "of Dexterity", "of Constitution", "of Wisdom"]

        #How much each rarity adds to the base stat
        self.prefix_modifier =  {"Common":1, "Uncommon": 3, "Rare":6, "Epic": 9, "Legendary": 14, "Godly": 25}
        self.postfix_modifier =  {'':None,"of Strength":"STR", "of Intelligence":"INT", "of Dexterity":"DEX", "of Constitution":"CON", "of Wisdom":"WIS"}


        #loot_type protocol: "name": (x_start,x_end,y), x and y being tile cordinates in the spritesheet
        self.loot_types = {
            "Poleaxe": (1,8,11),
            "Projectile": (0,3,10),
            "Spear": (4,10,10),
            "Dagger": (11,15,10),
            "Sword": (29,34,10),
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

    #-----------------
    #Generate Wearable
    #-----------------
    def generate_wearable(self, loot_type,loot_rarity):
        #Base values for item
        item_name = loot_type[0]
        loot_tile = random.randint(loot_type[1][0],loot_type[1][1])

        #Create Item
        item = Item(0,0,item_name,loot_tile,loot_type[1][2])
        item.equippable = True

        #Get rarity prefix and modifier postfix
        item_prefix = ""
        for rarity in self.prefixes:
            if loot_rarity >= self.prefixes[rarity][0] and loot_rarity <= self.prefixes[rarity][1]:
                item_prefix = rarity

        item_postfix = self.postfixes[random.randint(0,len(self.postfixes)-1)]

        #Add stat modifier
        stat = self.postfix_modifier[item_postfix]
        modifier = self.prefix_modifier[item_prefix]

        curse_or_blessed = random.choice(["+","+","+","+","+","-"])
        if curse_or_blessed == "-":
            item.cursed = True
        else:
            item.blessed = True

        #add stats
        if stat != None:
            item.stat_modifier = [f"{stat}{curse_or_blessed}{modifier}"]

        item.name = f"{item_prefix} {item_name} {item_postfix}"
        return item
    
    #-----------------
    #Generate Weapon
    #-----------------
    def generate_weapon(self, loot_type, loot_rarity):
        #Base values for item
        item_name = loot_type[0]
        loot_tile = random.randint(loot_type[1][0],loot_type[1][1])

        #Create Item
        item = Item(0,0,item_name,loot_tile,loot_type[1][2])
        item.equippable = True
        
        #Get rarity prefix and modifier postfix
        item_prefix = ""
        for rarity in self.prefixes:
            if loot_rarity >= self.prefixes[rarity][0] and loot_rarity <= self.prefixes[rarity][1]:
                item_prefix = rarity

        item_postfix = self.postfixes[random.randint(0,len(self.postfixes)-1)]

        #Add stat modifier
        stat = self.postfix_modifier[item_postfix]
        modifier = self.prefix_modifier[item_prefix]

        curse_or_blessed = random.choice(["+","+","+","+","+","-"])
        if curse_or_blessed == "-":
            item.cursed = True
        else:
            item.blessed = True


        #add stats, damagebase stat for weapon
        if stat != None:
            item.stat_modifier = [f"{stat}{curse_or_blessed}{modifier}"]

        item.stat_modifier.append(f"DMG+{modifier}")

        item.name = f"{item_prefix} {item_name} {item_postfix}"
        return item

    #-----------------
    #Generate Consumable
    #-----------------
    def generate_consumable(self, loot_type, loot_rarity):
        
        #Base values for item
        item_name = loot_type[0]
        loot_tile = random.randint(loot_type[1][0],loot_type[1][1])

        #Create Item
        item = Item(0,0,item_name,loot_tile,loot_type[1][2])
        item.consumable = True

        #Get rarity prefix and modifier postfix
        item_prefix = ""
        for rarity in self.prefixes:
            if loot_rarity >= self.prefixes[rarity][0] and loot_rarity <= self.prefixes[rarity][1]:
                item_prefix = rarity

        item_postfix = self.postfixes[random.randint(0,len(self.postfixes)-1)]

        curse_or_blessed = random.choice(["+","+","-"])
        if curse_or_blessed == "-":
            item.cursed = True
        else:
            item.blessed = True

        #Base stat
        stat = self.postfix_modifier[item_postfix]
        #Roll stat +- (bigger chance for stat)
        modifier = self.prefix_modifier[item_prefix]

        item.stat_modifier = [f"{stat}{curse_or_blessed}{modifier}"]

        item.name = f"{item_prefix} {item_name} {item_postfix}"
        return item

    #-------------
    #Generate loot
    #-------------
    def get_random_loot(self):

        loot_type = random.choice(list(self.loot_types.items()))
        loot_tile = random.randint(loot_type[1][0],loot_type[1][1])
        loot_rarity = random.randint(0,100)

        item_prefix = ""

        print("loot roll", loot_rarity)
        item_postfix = self.postfixes[random.randint(0,len(self.postfixes)-1)]
        for rarity in self.prefixes:
            if loot_rarity >= self.prefixes[rarity][0] and loot_rarity <= self.prefixes[rarity][1]:
                item_prefix = rarity


        #Base Item and rarity
        base_item = loot_type[0]
        name = f"{item_prefix} {loot_type[0]} {item_postfix}"

        #Create Item
        item = Item(0,0,name,loot_tile,loot_type[1][2])
        item.description = f"a {loot_type[0]}"

        #Check what type of item

        #Potion is consumable, can only give +- HP
        if base_item == "Potion":
            item = self.generate_consumable(loot_type,loot_rarity)

        #Weapon
        elif base_item in ["Spear", "Poleaxe", "Dagger","Sword"]:
            item = self.generate_weapon(loot_type,loot_rarity)
        
        #Armor/wearables
        elif base_item in ["Sheild","Ring","Armor","Helmet","Head Cap","Cloak","Necklace","Gloves","Shoes"]:    
            item = self.generate_wearable(loot_type,loot_rarity)

        print(f"Generated loot of {item_prefix} quality!")
        return item


