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
        self.max_messages = 10
        self.action_texts = []


        #DOGSHIT solution but i dont want player to be owned by gui....
        self.inventory = []

    #---------------------------------------
    #Controller owns the GUI, the gui is generic
    #---------------------------------------
    def draw(self):

        self.draw_action_log()
        self.draw_inventory()

        for text, pos in self.texts:
            self.screen.blit(text, pos)


    #----------------------------------------
    #Adding a text at a position for this gui
    #----------------------------------------
    def add_text(self, text, pos, color=(255,50,50) ,size= 18):
        font = pygame.font.Font('freesansbold.ttf', size)
        self.texts.append([font.render(text, True, color),pos])

    def add_text_action_log(self, text):
        font = pygame.font.Font('freesansbold.ttf', 18)
        self.action_texts.append(font.render(text, True, (255,50,50)))     


    #---------------------------------------------
    #Action log for various happenings in the game
    #---------------------------------------------
    def draw_action_log(self):
        
        #Draw window rectangle
        window = pygame.Rect(0,0,260,260)
        window_border = pygame.Rect(0,0,260,260)

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





