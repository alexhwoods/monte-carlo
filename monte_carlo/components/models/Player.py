# Author Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Hand import Hand

class Player():



    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = None
        self.current_bet = None

    def set_hand(self, arr):
        self.hand = Hand(arr)

    def bet(self, amount = 0):
        if amount > self.chips:
            amount = self.chips
        self.current_bet = amount
        self.chips = self.chips - amount

    # if the player wins a round
    def increase_chips(self, amount):
        self.chips += amount

    def __str__(self):
        string = self.name + ", " + str(self.chips)
        return string
