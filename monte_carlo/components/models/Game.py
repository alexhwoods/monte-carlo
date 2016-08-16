# Author Alex Woods <alexhwoods@gmail.com>
import uuid
from pprint import pprint
from monte_carlo.components.models.Deck import Deck
from monte_carlo.components.models.Round import Round


class Game(object):

    def __init__(self, table_min=10):
        self.id = uuid.uuid4()

        self.deck = Deck()
        self.players = []
        self.pot = 0
        self.table_min = table_min
        self.round = None
        self.round_num = 0

    def add_player(self, player):
        self.players.append(player)

    def get_players(self):
        return self.players

    def end_round(self):
        cards = self.round.community_cards
        for player in self.players:
            for card in player.hand.cards: cards.append(card)
            player.folded = False

        self.deck.push_bottom(cards)
        if not self.deck.is_full():
            "Delete this if you never reach it"
            print("Reaching a problem statement")
            self.deck = Deck()

# TODO eventually delete this, but for now I'll keep them, just in case we need to quick test something. 
    # def test_betting(self):
    #     self.round = Round(self)    # constructor called right here
    #     self.deck.shuffle()
    #     self.round.deal_hole()
    #     self.round.flop()
    #     self.round.turn()
    #     self.round.river()
    #     self.round.showdown()
    #
    #     if self.round.over:
    #         print("Betting info: ")
    #         self.round.bet_manager.status()
    #         pprint({player.name: chips for player, chips in self.round.bet_manager.chips_at_beginning.items()})

    def run(self):
        self.deck.shuffle()
        self.round = Round(self)
        self.round_num += 1

        self.round.deal_hole()
        self.round.pre_flop()
        print()

        self.round.flop()
        self.round.post_flop()
        print()

        self.round.turn()
        self.round.post_turn()
        print()

        self.round.river()
        self.round.showdown()

        if self.round.over:
            self.round.bet_manager.distribute()

    def show(self):
        arr = []
        for i in self.players:
            arr.append(str(i))
        pprint(arr)
        print("The minimum table bet is " + str(self.table_min) + " chips.")
        print("\n")
        if self.round is not None:
            self.round.show_all()








