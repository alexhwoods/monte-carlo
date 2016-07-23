# Author Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Deck import Deck
from monte_carlo.components.models.Player import Player
from pprint import pprint

class Game(object):

    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.pot = 0

    def add_player(self, player):
        self.players.append(player)

    def start_round(self):

        for i in self.players:
            self.deck.draw(2)


    def show(self):
        arr = []
        for i in self.players:
            arr.append(str(i))
        pprint(arr)
        print("\n")



# Testing

game = Game()
game.add_player(Player("Carla", 200))
game.show()


