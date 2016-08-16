# Author Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Hand import Hand
from monte_carlo.components.managers.BetManager import BetManager

from pprint import pprint

stages = ['HOLE', 'FLOP', 'TURN', 'RIVER']
betting_stages = ['PRE_FLOP', 'POST_FLOP', 'POST_TURN', 'SHOWDOWN']

class Round(object):
    """ See Round.md for a complete guide to this class.
    """


    def __init__(self, game):
        self.players = game.players
        self.deck = game.deck
        self.community_cards = []
        self.table_min = game.table_min
        self.stage = 'HOLE'
        self.over = False

        # purely for data saving purposes, to use the data later
        self.hands = None
        self.folded = None

    def next_stage(self):
        num = stages.index(self.stage)
        num += 1
        self.stage = stages[num]

    def deal(self):
        if self.stage == 'HOLE':
            for player in self.players:
                player.set_hand(self.deck.draw_many(2))
        elif self.stage == 'FLOP':
            self.community_cards = self.deck.draw_many(3)
        elif self.stage == 'TURN':
            turn = self.deck.draw_one()
            self.community_cards.append(turn)
        elif self.stage == 'RIVER':
            river = self.deck.draw_one()
            self.community_cards.append(river)
        else:
            pass

    # internal
    def make_data(self):
        hands = {}
        for player in self.players:
            hands[player] = player.hand

        self.hands = hands







