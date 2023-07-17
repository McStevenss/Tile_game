from twisted.internet import reactor, protocol
from twisted.internet.protocol import ClientFactory
import pickle
import json
from game import *
from player import *


class ClientProtocol(protocol.Protocol):
    player = None
    playerList = None
    game = None
    def __init__(self, player:Player, playerList, game:Game):
        self.player = player
        self.playerList = playerList
        self.game = game

    def connectionMade(self):
        print("Connected to the game server")
        self.factory.client_instance = self

    def dataReceived(self, data):
        # Handle the received data
        gameEvent = pickle.loads(data)
        #handle_connection(self.game, self.game.player, self.game.player_list, gameEvent)

    def connectionLost(self, reason):
        print("Disconnected from the game server")

    def sendData(self, data):
        self.transport.write(data)

class EchoClientFactory(protocol.ClientFactory):
    protocol = ClientProtocol

    def __init__(self, player, player_list, game):
        self.player = player
        self.player_list = player_list
        self.client_instance = None
        self.game = game

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed:', reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        print('Connection lost:', reason.getErrorMessage())

    def buildProtocol(self, addr):
        protocol_instance = self.protocol(self.player, self.player_list, self.game)
        protocol_instance.factory = self
        return protocol_instance
    
    def sendData(self, data):
        if self.client_instance and self.client_instance.transport:
            print("Factory got data")
            self.client_instance.sendData(data)
        else:
            print("Cannot send data. Connection not established.")

def connect_to_server(address, game):
    client_factory = EchoClientFactory(game.player,game.players, game)
    game.clientConnection = client_factory
    reactor.connectTCP(address, 4321, client_factory)