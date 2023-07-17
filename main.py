from game import *
from client import *

# if __name__ == '__main__':
#   game = Game()
#   game.run()

serverAddr = "127.0.0.1"

if __name__ == '__main__':
    game = Game()
    reactor.callWhenRunning(connect_to_server,serverAddr, game)
    reactor.callWhenRunning(game.run)
    reactor.run()