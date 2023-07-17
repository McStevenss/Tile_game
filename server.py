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
from server_tools import *

#Game classes
# from map import *
# from gui import *
# from player import *
# from controller import *
# from item import *
# from npc import *


BUFFERSIZE = 512
HEARTBEAT_INTERVAL = 5





def generate_existing_players(player_list):
    pass
    # existing_player_data = ['existing_players']
    # for key in player_list:
    #   player = player_list[key]
    #   existing_player_data.append([player.playerID ,player.name, player.x, player.y, player.Class, player.health, player.angle])

    # return existing_player_data

from twisted.internet import protocol, reactor

global players
global connections
connections = {}
players = {}

class MainServer(protocol.Factory):


    def __init__(self):
        print("Server initialized!")
        self.players = []
        self.connections = []

    def buildProtocol(self, addr):
      return SecondaryServer(self)

    def notifyPlayerDisconnected(self, player_id):
      # Handle the removal of the disconnected player
      print("Player", player_id, "has disconnected")
      if player_id in players:
          del players[player_id]
          for connection in connections.keys():
            connection.sendData(['remove_player', player_id])

    # def broadcastPlayerListUpdate(self):
    #   #self.send_message(['remove_player', self.player.playerID]
    #   player_data = [(player_id, player.name, player.x, player.y) for player_id, player in player_list.items()]
    #   message = ['player_list_update', player_data]

    #   for connection in self.connections.keys():
    #       connection.sendData(message)

    def generateExistingPlayers(self):
      return [(player_id, player.name, player.x, player.y) for player_id, player in self.player_list.items()]
    
    def parse_data(self,data):
      pass


class SecondaryServer(protocol.Protocol):
    factory = None

    def __init__(self, factory):
      print("Secondary server created!")
      self.factory = factory
      self.players = self.factory.players
      self.connections = self.factory.connections

    def connectionMade(self):
        playerid = len(players)
        
        # players[playerid] = player
        # connections[self] = playerid
        # g_player_id = g_player_id + 1
        print("A new player has connected with id:", playerid)

        # existing_player_data = generate_existing_players(player_list)
        # self.sendData(['id update', playerid,existing_player_data])

    def connectionLost(self, reason):
       print("Connection lost: ",reason)

    def dataReceived(self, data): 
        incomming_data = data.decode()       
        print("Recieved data: ", incomming_data)
        
        new_players = handle_incomming_message(incomming_data,self.players,self.connections)
        
        self.players = new_players

    def sendData(self, data):
      pass
      #self.transport.write(pickle.dumps(data))
    

# Create and start the server
factory = MainServer()
print("Server started...")
reactor.listenTCP(4321, factory, interface='127.0.0.1')
reactor.run()




