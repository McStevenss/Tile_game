import sys
 
import pygame
from pygame.locals import *
from spritesheet import *
from item import *
from map import *
from npc import *
import json


class Player():
    def __init__(self, spritesheet:Spritesheet, screen, map:Map, name="Unknown"):
        #Position & misc
        self.name=name
        self.x = 1
        self.y = 1
        self.health = 100
        self.local_player = False
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
        self.equipped = []

        #Stats
        self.level = 1
        self.experience = 0
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.weapon_damage = 1
        
    #------------
    #Update logic
    #------------
    def update(self):
        
        #Check if player is dead
        if self.health <= 0:
            self.tileCordinate_x = 16
            self.tileCordinate_y = 21


    #---------------------------------------------------
    #Packing neccesary player information to JSON object
    #---------------------------------------------------
    def pack_for_server(self, command=None):
        player_object = {
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "health": self.health,
            "inventory": [],
            "equipped": [],
            "tileCordinate_x": self.tileCordinate_x,
            "tileCordinate_y": self.tileCordinate_y,
            "level": self.level,
            "experience":self.experience,
            "strength":self.strength,
            "dexterity": self.dexterity,
            "constitution":self.constitution,
            "intelligence":self.intelligence,
            "wisdom": self.wisdom,
            "weapon_damage" :self.weapon_damage
        }

        #Handle items in inventory
        for item in self.inventory:
            player_object["inventory"].append(item.pack_for_server(usejson=False))
       
        #Handle equipped items
        for item in self.equipped:
            player_object["equipped"].append(item.pack_for_server(usejson=False))

        if command !=None:
            player_object["command"] = command

        return json.dumps(player_object, indent=4)


 
    #-------------------
    #Player draws itself
    #-------------------
    def draw(self):

        #If player is controlled locally, make map center around them
        if self.local_player:
            self.map.set_camera_offset(self.x * self.spritesheet.tilesize,self.y * self.spritesheet.tilesize, centered=self.local_player)

        self.map.drawEntity(self.x,self.y, (self.tileCordinate_x,self.tileCordinate_y),self)

    #--------------------------------
    #Player handles its own inventory
    #--------------------------------
    def add_item_to_inventory(self,item:Item):
        self.inventory.append(item)

    #-------------
    #Destroys item
    #-------------
    def remove_item_from_inventory(self,item:Item):
        self.inventory.remove(item)

    #-------------------------
    #Drops item from inventory
    #-------------------------

    def drop_item_from_inventory(self,item:Item):

        if item != None:
            self.inventory.remove(item)

            #Drop at adjacent tile, check if its avalible:
            if self.map.legalMove(self.x +1,self.y):
                item.x = self.x +1
                item.y = self.y
                self.map.add_item(item)
                return True
            
            elif self.map.legalMove(self.x -1,self.y):
                item.x = self.x -1
                item.y = self.y
                self.map.add_item(item)
                return True
            
            elif self.map.legalMove(self.x,self.y +1):
                item.x = self.x 
                item.y = self.y +1
                self.map.add_item(item)
                return True
            
            elif self.map.legalMove(self.x,self.y -1):
                item.x = self.x 
                item.y = self.y -1
                self.map.add_item(item)
                return True
        return False

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
    

    #----------------------------------------------------------
    #Set player to local, will make the camera center on player
    #----------------------------------------------------------
    def setLocal(self,isLocalPlayer):

        if isLocalPlayer:
            self.local_player = isLocalPlayer
            self.map.set_camera_offset(self.x * self.spritesheet.tilesize,self.y * self.spritesheet.tilesize, centered=isLocalPlayer)
        else:
            return
    

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
                
            if type(entity) == NPC:
                
                #Talk to friendly NPCs
                if entity.friendly:
                    chat_line = entity.chat()
                    return f"{entity.name}: {chat_line}"
                #Attack unfriendly NPCs
                else:
                    pass

    #------------------------
    #Update item in inventory
    #------------------------
    def update_item_in_inventory(self,item:Item):
        try:
            inventory_idx = self.inventory.index(item)
            self.inventory[inventory_idx] = item
            return True
        except:
            return False

    #-----------------------
    #Applies a stat increase
    #-----------------------
    def apply_stat(self,stat,ammount):

        if stat == "DMG":
            self.weapon_damage += ammount
        elif stat == "HP":
            self.health += ammount
        elif stat =="STR":
            self.strength += ammount
        elif stat == "LVL":
            self.level += ammount
        elif stat == "XP":
            self.experience += ammount
        elif stat == "DEX":
            self.dexterity += ammount
        elif stat == "CON":
            self.constitution += ammount
        elif stat == "INT":
            self.intelligence += ammount
        elif stat == "WIS":
            self.wisdom += ammount

        return
    

    #----------
    #Parse stat
    #----------
    def parse_stat(self,stat, inverse=False):

        if inverse == False:
            if "+" in stat:   
                parsed_stat = stat.split("+")
                return parsed_stat[0], int(parsed_stat[1])
            else:
                parsed_stat = stat.split("-")
                return parsed_stat[0], -int(parsed_stat[1])
        else:
            if "+" in stat:   
                parsed_stat = stat.split("+")
                return parsed_stat[0], -int(parsed_stat[1]) 
            else:
                parsed_stat = stat.split("-")
                return parsed_stat[0], +int(parsed_stat[1])


    #--------------------
    #Apply item modifiers, will return the action used
    #--------------------
    def use_item(self,item:Item):
        stats,consumable,equippable = item.use()

        # #Connect modifiers with players
        # stat_map = {"DMG":self.weapon_damage,
        #             "HP": self.health,
        #             "STR":self.strength,
        #             "LVL":self.level,
        #             "XP": self.experience,
        #             "DEX":self.dexterity,
        #             "CON":self.constitution,
        #             "INT":self.intelligence,
        #             "WIS":self.wisdom}
        
        
        #Consume consumable
        if consumable:
            #apply stats
            for stat in stats:
                    stat, ammount = self.parse_stat(stat)
                    self.apply_stat(stat, ammount)

            #remove item after use because its consumable
            self.remove_item_from_inventory(item)
            return "[D]"
        
        #Equip item
        #Important to add stats when equipped
        if equippable and item.isequipped == False:
            #apply stats that item gives
            for stat in stats:
                stat, ammount = self.parse_stat(stat)
                self.apply_stat(stat, ammount)


            #update item is equipped
            item.isequipped = True
            self.update_item_in_inventory(item)
            self.equipped.append(item)

            if item.blessed:
                return "[E]"
            else:
                return "[E][c]"

        #Unequip item
        #Remove stats!  
        if equippable and item.isequipped == True:       
            #apply stats that item gives (Now reversed)
            for stat in stats:
                stat, ammount = self.parse_stat(stat,inverse=True)
                self.apply_stat(stat, ammount)

                    
            item.isequipped = False
            self.update_item_in_inventory(item)
            self.equipped.remove(item)
            if item.blessed:
                return "[U]"
            else:
                return "[U][c]"

