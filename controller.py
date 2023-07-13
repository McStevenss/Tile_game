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
        self.gui.add_text(f"Health: {self.player.health}",(315,15),size=25)

        #Bad solution
        self.player.setLocal(True)

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


            #Inventory
            if event.key == K_i:
                self.gui.show_inv_cursor = not self.gui.show_inv_cursor

            if self.gui.show_inv_cursor:

                if event.key == K_RIGHT:
                    self.gui.move_cursor(dx=1)

                if event.key == K_LEFT:
                    self.gui.move_cursor(dx=-1)

                if event.key == K_UP:
                    self.gui.move_cursor(dy=-1)

                if event.key == K_DOWN:
                    self.gui.move_cursor(dy=1)

                #Inspect item
                if event.key == K_RETURN:
                    item = self.gui.get_item_at_cursor()
                    self.gui.add_text_action_log(f"{item.name if item != None else 'Hmm?'}")

                #Drop item
                if event.key == K_DELETE:
                    item = self.gui.get_item_at_cursor()

                    if item == None:
                        self.gui.add_text_action_log(f"I cannot drop that")
                    else:
                        if self.player.drop_item_from_inventory(item):
                            self.gui.add_text_action_log(f"-{item.name}")
                        else:
                            self.gui.add_text_action_log(f"No space to drop that")
                        

                #Equip/use
                # if event.key == K_RETURN:
                #     item = self.gui.get_item_at_cursor()
                #     self.gui.add_text_action_log(f"{item.name if item != None else 'Hmm?'}")


            #Check if where player have walked contains loot
            isLoot, item = self.player.check_for_loot()
            if isLoot:
                self.gui.add_text_action_log(f"+{item.name}")
            




