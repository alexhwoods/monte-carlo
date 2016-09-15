# Author Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Hand import Hand
from monte_carlo.components.managers.BetManager import BetManager


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

        # if deal is accidentally called twice, we don't want hands to be overwritten
        self.stage_dealt = {stage: False for stage in stages}

    def deal(self):
        if self.stage == 'HOLE' and self.stage_dealt['HOLE'] is False:
            for player in self.players:
                player.set_hand(self.deck.draw_many(2))

            self.stage_dealt['HOLE'] = True
            self.stage = 'FLOP'

        elif self.stage == 'FLOP' and self.stage_dealt['FLOP'] is False:
            self.community_cards = self.deck.draw_many(3)
            self.stage_dealt['FLOP'] = True
            self.stage = 'TURN'

        elif self.stage == 'TURN' and self.stage_dealt['TURN'] is False:
            turn = self.deck.draw_one()
            self.community_cards.append(turn)
            self.stage_dealt['TURN'] = True
            self.stage = 'RIVER'

        elif self.stage == 'RIVER' and self.stage_dealt['RIVER'] is False:
            river = self.deck.draw_one()
            self.community_cards.append(river)
            self.stage_dealt['RIVER'] = True

            # no need to set self.stage to anything, if deal() is called nothing will happen since round has been
            # dealt.

        else:
            pass

    # internal
    def make_data(self):
        hands = {}
        for player in self.players:
            hands[player] = player.hand

        self.hands = hands







