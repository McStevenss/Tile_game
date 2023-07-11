import sys
 
import pygame
from pygame.locals import *
from spritesheet import *
from item import *

class Map:
    def __init__(self, spritesheet, screen, draw_center):

        #Rendering
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.spritesheet = spritesheet
        self.draw_center = draw_center

        #Map
        # self.map_data = [
        #     [1,1,1,1,1,1,1,1,1,1,1],
        #     [1,0,0,0,0,0,0,0,0,0,1],
        #     [1,0,0,0,0,0,0,0,0,0,1],
        #     [1,0,0,0,0,0,0,0,0,0,1],
        #     [1,0,0,0,0,0,0,0,0,0,1],
        #     [1,1,1,2,1,0,1,1,1,2,1],
        #     [1,0,0,0,1,0,1,0,0,0,1],
        #     [1,0,0,0,1,0,1,0,0,0,1],
        #     [1,1,1,1,1,1,1,1,1,1,1],
        # ]

        self.map_data = self.read_map_from_file("test.txt")
        

        #Misc
        self.wall_tiles = [1]
        self.items = []
        self.walkable_tiles = self.get_walkable_tiles()
        self.entities = []

    def read_map_from_file(self,path):
        f = open(path, "r")
        map = f.readlines()
        
        for idx, row in enumerate(map):
            map[idx] = row.replace(' \n','')
            map[idx] = map[idx].split(',')
            map[idx] = [eval(i) for i in map[idx]]

        print("read map from file:")
        for row in map:
            print(row)
        return map

    def draw(self):   
        #Floor color
        self.screen.fill((71,108,108))

        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):               
                screen_x, screen_y = self.convertPos(x,y)

                if tile == 1:
                    self.screen.blit(self.spritesheet.image_at(31,20), (screen_x,screen_y))

                #Create door
                if tile == 2:        
                    #Check if entity has been created or not
                    entity = self.getEntity(x,y)
                    if entity != None and type(entity) == Door:
                        #Entity already exists
                        self.drawEntity(x,y,(entity.tileX,entity.tileY),entity)
                    else:
                        #Entity hasnt been created
                        door = Door(x,y)
                        self.drawEntity(x,y,(door.tileX,door.tileY),door)

                #Path
                if tile == 9:
                    self.screen.blit(self.spritesheet.image_at(9,21), (screen_x,screen_y))

                if tile == 3:
                    self.screen.blit(self.spritesheet.image_at(3,21), (screen_x,screen_y))

        #After map is drawn, draw items that the map contains
        for item in self.items:
            screen_x, screen_y = self.convertPos(item.x,item.y)
            self.screen.blit(self.spritesheet.image_at(item.tileX,item.tileY), (screen_x,screen_y))



    #--------------------------------------------------
    #function to get if a certain cordinate is moveable
    #--------------------------------------------------
    def legalMove(self,x,y):
        pos = (x,y)

        #Loop through entities
        for x,y,entity in self.entities:

            #Ignore players
            if pos == (x,y) and type(entity).__name__ != "Player":
                #If door is opened, then its walkable
                if type(entity).__name__ == "Door" and entity.locked == False:
                    return True
                return False

        #Loop through map
        if pos in self.walkable_tiles:
            return True
        
        return False


    #------------------------------------------------
    #draw function for manipulating the base map data
    #------------------------------------------------
    def drawTile(self, x,y,tileID):
        #assuming all rows are the same lenght
        if y <= len(self.map_data) and x <= len(self.map_data[0]):
            self.map_data[y][x] = tileID


    #-----------------------------------------------------------------------------------------------------------------
    #function to get avalible tiles which are not walls. Preferably do this only at init or when map-layout is updated
    #-----------------------------------------------------------------------------------------------------------------
    def get_walkable_tiles(self):
        walkable_tiles = []
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile not in self.wall_tiles:
                    walkable_tiles.append((x,y))
        
        return walkable_tiles


    #-------------------------------------------------------------
    #function to handle position conversion if draw_center is true
    #-------------------------------------------------------------
    def convertPos(self,x,y):
        if self.draw_center:
            screen_y = y * self.spritesheet.tilesize + (self.screen_height // 2) - ((len(self.map_data) * self.spritesheet.tilesize) // 2)
            screen_x = x * self.spritesheet.tilesize + (self.screen_width // 2) - ((len(self.map_data[0]) * self.spritesheet.tilesize) // 2)
        else:
            screen_y = y * self.spritesheet.tilesize
            screen_x = x * self.spritesheet.tilesize

        return screen_x,screen_y
    

    #-------------------------------------------
    #Generic separate draw function for Entities (anything thats not a wall)
    #-------------------------------------------
    def drawEntity(self,x,y, spriteTile, entity):
        screen_x, screen_y = self.convertPos(x,y)
        self.screen.blit(self.spritesheet.image_at(spriteTile[0],spriteTile[1]), (screen_x,screen_y))
        self.entities.append((x,y,entity))

    
    #-----------------------------------
    #Getting entity on map at cordinates
    #-----------------------------------
    def getEntity(self,x,y):
        for e_x,e_y,entity in self.entities:
            if e_x == x and e_y == y:
                return entity
        return None


    #----------------------------------------------------------------------------------
    #It makes sense that each map (if multiple) would contain the loot/items for itself
    #----------------------------------------------------------------------------------
    def add_item(self, item:Item):
        self.items.append(item)

    def remove_item(self, item:Item):
        self.items.remove(item)

    def get_item(self, x, y):
        #Look at every item in the map and see if it is at the specified location
        for item in self.items:
            if item.x == x and item.y == y:
                return item
        
        #No item is at this location on the map
        return None




    



