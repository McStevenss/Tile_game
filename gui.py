import sys
 
import pygame
from pygame.locals import *
from spritesheet import *
from map import *


class Gui:
    def __init__(self, spritesheet, screen):

        #Rendering
        self.screen = screen
        self.spritesheet = spritesheet
        
        #Gui Text
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.texts = []
        
        #Action log
        self.max_messages = 13
        self.action_texts = []

        #Inventory Navigation
        self.show_inv_cursor = False
        self.cursor_x = 0
        self.cursor_y = 0


        #DOGSHIT solution but i dont want player to be owned by gui....
        self.inventory = []
        self.stats = []

    #---------------------------------------
    #Controller owns the GUI, the gui is generic
    #---------------------------------------
    def draw(self):
        self.texts = []

        self.draw_action_log()
        self.draw_inventory()
        self.draw_stats()

        for text, pos in self.texts:
            self.screen.blit(text, pos)


    #----------------------------------------
    #Adding a text at a position for this gui
    #----------------------------------------
    def add_text(self, text, pos, color=(255,50,50) ,size= 18):
        font = pygame.font.Font('freesansbold.ttf', size)
        self.texts.append([font.render(text, True, color),pos])

    def add_text_action_log(self, text):
        font = pygame.font.Font('freesansbold.ttf', 15)
        self.action_texts.append(font.render(text, True, (255,50,50)))     


    #---------------------------------------------
    #Action log for various happenings in the game
    #---------------------------------------------
    def draw_action_log(self):
        
        #Draw window rectangle
        window = pygame.Rect(0,0,270,260)
        window_border = pygame.Rect(0,0,270,260)

        pygame.draw.rect(self.screen, (30,30,30), window)
        pygame.draw.rect(self.screen, (255,255,255), window_border,2)

        if len(self.action_texts) > self.max_messages:
            self.action_texts.pop(0)

        #Populate with texts
        for idx, text in enumerate(self.action_texts):
            pos = (15, 18* idx + 18)
            self.screen.blit(text, pos)


    #---------------------------------------
    #Inventory, supply list of items to draw
    #---------------------------------------
    def draw_inventory(self):

        #Max tiles W/H
        max_icons_width = 8
        max_icons_heigth = 8

        #Draw inventory rectangle
        inventory = pygame.Rect(0,265,260,260)
        inventory_border = pygame.Rect(0,265,260,260)

        pygame.draw.rect(self.screen, (30,30,30), inventory)
        pygame.draw.rect(self.screen, (255,255,255), inventory_border,2)

        #populate inventory GUI
        new_row = 0
        for idx, item in enumerate(self.inventory):
            if idx >= max_icons_width:
                new_row = idx // max_icons_width
            
            #Make values loop when a row is filled
            inv_x = (idx % max_icons_width) * 32 + 2
            inv_y = 268 + (new_row * 32)

            #Draw item in inventory
            item_img = self.spritesheet.image_at(item.tileX,item.tileY)
            self.screen.blit(item_img, (inv_x,inv_y))

            #Indicate if its equipped
            #print("gui, item equipped",item.isequipped)
            if item.isequipped:
                equip_rect = pygame.Rect(inv_x,inv_y,32,32)
                pygame.draw.rect(self.screen, (59,181,65), equip_rect,2)


        #SELECTOR
        if self.show_inv_cursor:
            selector = pygame.Rect(self.cursor_x*32 + 2, 268 + (self.cursor_y * 32),32,32)
            pygame.draw.rect(self.screen, (255,255,255), selector,2)

    #-------------
    #Draw stat box
    #-------------
    def draw_stats(self):
        
        stats_window = pygame.Rect(0,530,260,230)
        stats_window_border = pygame.Rect(0,530,260,230)

        pygame.draw.rect(self.screen, (30,30,30), stats_window)
        pygame.draw.rect(self.screen, (255,255,255), stats_window_border,2)

        #Print stats
        self.add_text(f"Level: {self.stats[0]}",(4,535))
        self.add_text(f"XP: {self.stats[1]}",(4,535 + 17*1))
        self.add_text(f"HP: {self.stats[2]}",(4,535 + 17*2))
        self.add_text(f"DMG: {self.stats[3]}",(4,535 + 17*3))
        
        self.add_text(f"STR: {self.stats[4]}",(4,535 + 20*4), (181,65,19))
        self.add_text(f"DEX: {self.stats[5]}",(4,535 + 20*5), (255,208,0))
        self.add_text(f"CON: {self.stats[6]}",(4,535 + 20*6), (255,0,233))
        self.add_text(f"INT: {self.stats[7]}",(4,535 + 20*7), (0,119,255))
        self.add_text(f"WIS: {self.stats[8]}",(4,535 + 20*8), (45,66,255))

    #------------------
    #Navigate inventory
    #------------------
    def move_cursor(self,dx=0,dy=0):

        MAX_TILE = 7

        self.cursor_x +=dx
        self.cursor_y +=dy

        if self.cursor_x > MAX_TILE or self.cursor_x < 0:
            self.cursor_x = 0
        
        if self.cursor_y > MAX_TILE or self.cursor_y < 0:
            self.cursor_y = 0

    def get_item_at_cursor(self):
        max_icons_width = 8
        inv_idx = self.cursor_x + (self.cursor_y * max_icons_width) 

        if inv_idx > len(self.inventory)-1:
            return None
        else:
            return self.inventory[inv_idx]
        
      

        
        





