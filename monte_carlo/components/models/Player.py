# Author Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Hand import Hand


class Player(object):

    def __init__(self, name, chips, computer=False):
        self.name = name
        self.chips = chips
        self.hand = None
        self.current_bet = None
        self.folded = False
        self.computer = computer

    def set_hand(self, arr):
        self.hand = Hand(arr)

    def bet(self, amount=0):
        if amount > self.chips:
            amount = self.chips
        self.current_bet = amount
        self.chips = self.chips - amount

    def fold(self):
        self.folded = True

    # if the player wins a round
    def win(self, amount):
        self.chips += amount

    def __str__(self):
        string = self.name + ", " + str(self.chips)
        return string
