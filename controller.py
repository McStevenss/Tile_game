import sys
 
import pygame
from pygame.locals import *
from spritesheet import *
from player import *
from gui import *



#This class controls a submitted player
#This class only controls logic, no drawing. the player class draws itself
#It also has access to the gui

class Controller():
    def __init__(self, player:Player, gui:Gui):
        self.player = player
        self.gui = gui


    #Updating player and listening to keypresses
    def update(self):
        self.gui.inventory = self.player.inventory
        self.gui.add_text(f"Health: {self.player.health}",(265,15),size=25)


    def handle_Keypress(self,event):
        if event.type == KEYUP and self.player.health > 0:
            
            if event.key == K_a:
                if self.player.map.legalMove(self.player.x-1,self.player.y):
                    self.player.x -=1
                else:
                    action = self.player.interract_entity(self.player.x-1,self.player.y)
                    self.gui.add_text_action_log(f"{action if action != None else 'Hmm?'}")
                     
            if event.key == K_d:
                if self.player.map.legalMove(self.player.x+1,self.player.y):
                    self.player.x +=1
                else:
                    action = self.player.interract_entity(self.player.x+1,self.player.y)
                    self.gui.add_text_action_log(f"{action if action != None else 'Hmm?'}")

            if event.key == K_w:
                if self.player.map.legalMove(self.player.x,self.player.y-1):
                    self.player.y -=1
                else:
                    action = self.player.interract_entity(self.player.x,self.player.y-1)
                    self.gui.add_text_action_log(f"{action if action != None else 'Hmm?'}")

            if event.key == K_s:
                if self.player.map.legalMove(self.player.x,self.player.y+1):
                    self.player.y +=1
                else:
                    action = self.player.interract_entity(self.player.x,self.player.y+1)
                    self.gui.add_text_action_log(f"{action if action != None else 'Hmm?'}")

            #Check if where player have walked contains loot
            isLoot, item = self.player.check_for_loot()
            if isLoot:
                self.gui.add_text_action_log(f"+{item.name}")
            




