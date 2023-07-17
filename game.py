import sys
from twisted.internet import reactor
import pygame
from pygame.locals import *
from spritesheet import *
from map import *
from gui import *
from player import *
from controller import *
from item import *
from npc import *

class Game:
    def __init__(self):
        pygame.init()
        self.clientConnection = None
        self.sent_player_info = False
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
        self.players = []
        self.controller = Controller(self.player, self.gui)
        


        # self.gui.add_text("This is a test text #1", (15,0))
        # self.gui.add_text("This is a test text #2", (15,33))

        #DEBUG
        item0 = Item(2,1,name="Key",tileX=32,tileY=14)
        item1 = Item(3,1,name="Key",tileX=32,tileY=14)
        item2 = Item(4,1,name="Key",tileX=32,tileY=14)
        item3 = Item(5,1,name="Key",tileX=32,tileY=14)
        item4 = Item(6,1,name="Key",tileX=32,tileY=14)
        item5 = Item(7,1,name="Key",tileX=32,tileY=14)
        item6 = Item(8,1,name="Key",tileX=32,tileY=14)
        item7 = Item(9,1,name="Key",tileX=32,tileY=14)
        item8 = Item(10,1,name="Key",tileX=32,tileY=14)



        loot = [item0,item1,item2,item3,item4,item5,item6,item7,item8]
       
        for item in loot:
            self.map.add_item(item)

        
        self.test_npc = NPC(self.map, 10,10,"George", 100, True)

        #/DEBUG
        self.send_message(self.player.pack_for_server())




    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                reactor.stop()
                pygame.quit()
                sys.exit()

            self.controller.handle_Keypress(event)

    def draw(self):

        self.map.draw()
        self.gui.draw()
        self.player.draw()

        self.test_npc.draw()
        pygame.display.flip()
        self.fpsClock.tick(self.fps)

    def update(self):
        self.controller.update()
        self.player.update()


        #Give server player info
        if self.sent_player_info == False:
            player_data = self.player.pack_for_server(command="new_player")
            didSend = self.send_message(player_data)
            if didSend:
                self.sent_player_info = True
                print("Sent player info")

        reactor.iterate()

    def run(self):
        #Game loop
        while True:
            self.update()
            self.check_events()
            self.draw()


    def send_message(self, message):
        if self.clientConnection and self.clientConnection.client_instance:      
            self.clientConnection.client_instance.sendData(message.encode())
            return True   
        else:
            print("Not connected to the server yet. Message not sent.")
            return False