# Author Alex Woods <alexhwoods@gmail.com>
import uuid
from monte_carlo.components.models.Deck import Deck
from monte_carlo.components.models.Round import Round
from monte_carlo.components.managers.BetManager import BetManager


class Game(object):

    def __init__(self, table_min=10):
        self.id = uuid.uuid4()

        self.deck = Deck()
        self.players = []
        self.bm = BetManager()
        self.table_min = table_min

        self.rounds = []
        self.over = False

    def add_player(self, player):
        self.players.append(player)

    def get_players(self):
        return self.players

    def newRound(self):
        self.deck = Deck()
        self.deck.shuffle()

        round = Round(self)
        self.rounds.append(round)

    def getCurrentRound(self):
        return self.rounds[-1]

    def endCurrentRound(self):
        round = self.rounds[-1]
        for player in self.players:
            player.hand = None
        # giving the chips to those that won them
        self.bet_manager.distribute()
        round.over = True
        self.bet_manager.reset()

    def isOver(self):
        chips = [player.chips for player in self.players]
        chips = [x for x in chips if x != 0]

        # if there is only one or less players who have a non-zero amount of chips, game is over
        return len(chips) <= 1 or self.over

    def winner(self):
        if self.isOver():
            chips = {player: player.chips for player in self.players}
            winners = max(chips, key=chips.get)
            return winners
        else:
            return None










