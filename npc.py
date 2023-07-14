import sys
 
import pygame
from pygame.locals import *
from spritesheet import *
import random
from map import *

class NPC():
    def __init__(self, map:Map ,x=0 ,y=0 ,name="NPC" ,health = 100 ,friendly=True , tileCordinate_x=38, tileCordinate_y=6):
        
        #Graphics
        self.x = x
        self.y = y

        self.tileCordinate_x = tileCordinate_x
        self.tileCordinate_y = tileCordinate_y

        self.map = map

        self.name = name
        self.description = "A npc"
        
        self.chat_line_idx = 0
        self.chat_lines = [f"Im {self.name}!","Hi there!", "Im a default npc!", "whats up?"]
        self.friendly = friendly
        self.health = health

    def chat(self):
        
        chat_line = self.chat_lines[self.chat_line_idx]
        self.chat_line_idx += 1
        if self.chat_line_idx >= len(self.chat_lines):
            self.chat_line_idx = 0

        return chat_line

    def update(self):
        pass

    def draw(self):
        self.map.drawEntity(self.x,self.y, (self.tileCordinate_x,self.tileCordinate_y),self)