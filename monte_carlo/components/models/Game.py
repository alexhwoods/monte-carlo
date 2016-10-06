# Author Alex Woods <alexhwoods@gmail.com>
import uuid
from components.models.Deck import Deck
from components.models.Round import Round
from components.managers.BetManager import BetManager


class Game(object):

    def __init__(self, table_min=10):
        self.id = uuid.uuid4()

        self.deck = Deck()
        self.players = []
        self.table_min = table_min
        self.bm = None
        self.rounds = []
        self.started = False
        self.over = False

    def start(self):
        self.bm = BetManager(self)
        self.started = True
        self.newRound()

    def add_player(self, player):
        self.players.append(player)


    def get_players(self):
        return self.players

    def newRound(self):
        self.deck = Deck()
        self.deck.shuffle()

        # folding reset
        for player in self.players:
            player.folded = False

        if len(self.rounds) > 0:
            previous_round = self.rounds[-1]
            if previous_round.over:
                round = Round(self)
                self.rounds.append(round)
                return True
            else:
                return False

        else:
            round = Round(self)
            self.rounds.append(round)
            return True


    def getCurrentRound(self):
        return self.rounds[-1]

    def endCurrentRound(self):
        round = self.rounds[-1]
        if not round.over:
            # giving the chips to those that won them
            self.bm.distribute()

            for player in self.players:
                player.hand = None
            
            round.over = True
            self.bm.reset()
            return True
        return False

    def isOver(self):
        if self.players == []:
            # (I had this problem earlier)
            print("There are no players in this game!")
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

    def toSimple(self):
    	gs = GameSimple(self)
    	return gs


# 		 information for the front end to work, but none of the inner details,
# 		 such as the bet manager.

class GameSimple():
	def __init__(self, game):
		self.id = str(game.id)
		self.players = game.players
		self.table_min = game.table_min
		self.num_rounds = len(game.rounds)






