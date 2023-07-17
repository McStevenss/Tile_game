import socket
import asyncore
import random
import pickle
import time
#from server_utils import handle_message

import threading


#NEW SERVER PORT
from twisted.internet import reactor, protocol
from twisted.protocols import basic
import json

BUFFERSIZE = 512
HEARTBEAT_INTERVAL = 5

class Player_lite():
    def __init__(self, name="unknown", health = 100, x = 1, y = 1, inventory = [], tileX = 4, tileY = 6):
        self.name=name
        self.health=health
        self.x = x
        self.y = y
        self.inventory = inventory
        self.tileX = tileX
        self.tileY = tileY

        self.level = 1
        self.experience = 0
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.weapon_damage = 1

def handle_incomming_message(message,players,connections):
    
    data:dict = json.loads(message)
    if "command" in data.keys():
        
        #check command
        if data["command"] == "new_player":
            
            #new player!
            new_player = Player_lite(data["name"], data["health"], data["x"], data["y"], tileX=data["tileCordinate_x"],tileY=data["tileCordinate_y"])
            players.append([data["name"],new_player])


            print("New player created")
            return players