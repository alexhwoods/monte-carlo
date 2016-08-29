# Author Alex Woods <alexhwoods@gmail.com>
import uuid
from monte_carlo.components.models.Hand import Hand


class Player(object):

    def __init__(self, name, chips, computer=False):
        self.name = name
        self.id = uuid.uuid4()
        self.chips = chips
        self.hand = None
        self.best_hand = None
        self.current_bet = None
        self.folded = False
        self.computer = computer

        # This will be reset every round to keep searching it from being expensive
        # TODO: reset it
        self.bets = []

    def set_hand(self, arr):
        self.hand = Hand(arr)

    # gonna keep the betting logic in BetManager
    def set_chips(self, amount):
        self.chips = amount

    def fold(self):
        self.folded = True

    # if the player wins a round
    def win(self, amount):
        self.chips += amount

    def __str__(self):
        string = self.name + " (" + str(self.chips) + ')'
        return string




