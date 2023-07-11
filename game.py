import sys
 
import pygame
from pygame.locals import *
from spritesheet import *
from map import *
from gui import *
from player import *
from controller import *
from item import *

class Game:
    def __init__(self):
        pygame.init()

        #Fps
        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        #Screen settings
        self.width = 1360
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.draw_center = True
        pygame.display.set_caption('Hausen Klatscher')

        #Classes
        self.spritesheet = Spritesheet("X11tiles-32-32.png",self.screen)
        self.map = Map(self.spritesheet, self.screen, True)
        self.gui = Gui(self.spritesheet, self.screen)
        self.player = Player(self.spritesheet, self.screen, self.map)
        self.controller = Controller(self.player, self.gui)


        # self.gui.add_text("This is a test text #1", (15,0))
        # self.gui.add_text("This is a test text #2", (15,33))

        #DEBUG
        item = Item(3,3,name="Boots Of Speed")
        item2 = Item(4,3,name="Ring Of Icarus",tileX=0,tileY=14)
        item3 = Item(5,3,name="X-ray googles",tileX=3,tileY=15)

        item10 = Item(5,1,name="Key",tileX=32,tileY=14)
        item11 = Item(1,6,name="Key",tileX=32,tileY=14)


        loot = [item,item2,item3,item10,item11]
       
        for item in loot:
            self.map.add_item(item)

        
        #/DEBUG




    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            self.controller.handle_Keypress(event)

    def draw(self):

        self.map.draw()
        self.gui.draw()
        self.player.draw()
        pygame.display.flip()
        self.fpsClock.tick(self.fps)

    def update(self):
        self.controller.update()
        self.player.update()

    def run(self):
        #Game loop
        while True:
            self.update()
            self.check_events()
            self.draw()