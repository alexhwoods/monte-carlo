# Author Alex Woods <alexhwoods@gmail.com>
from components.models.Hand import Hand
from components.models.Player import Player

class Pot(object):
    ''' While you might think Pot is not important enough to be an attribute, if we give it object level status,
        it can make the design a lot neater. That's because of side pots.

        Imagine you have 3 players, player A, B, and C. A has $25, B has $50, and C has $75. In the main pot, in which
        everyone is included, it can only get as high as $75 ($25 per person). Then B and C will start a side pot if
        they want to continue betting.

        Player C can't bet any more than $25 into this pot, since he's limited by the amount player B has (well he can
        bet more, but it will be immediately returned).


        Then, in the showdown (the revealing of the cards), the main pot is decided by the best hand out of all 3
        players, and the side pot is decided between the best hand between players B and C.
    '''

    def __init__(self, players, max_per_player):
        self.players = players
        self.counts = {player: 0 for player in self.players}

        self.max_per_player = max_per_player

        # note that a pot should not be maxed until all players have added either all their
        # remaining chips or the maximum amount to it
        self.is_maxed = False

    def add(self, player, amount):
        if self.counts[player] + amount <= self.max_per_player:
            self.counts[player] += amount
        else:
            self.counts[player] = self.max_per_player

    def get_amount(self):
        return sum([chips for player, chips in self.counts.items()])

    # DON'T DELETE (it breaks the equality operator)
    def __hash__(self):
        return hash(self.__dict__.values())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        string = str("Max = " + str(self.max_per_player) + "\n")
        string += "Current State - "
        string += str({player.name: self.counts[player] for player in self.players})
        return string
