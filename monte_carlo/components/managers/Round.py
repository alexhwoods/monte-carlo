# Author Alex Woods <alexhwoods@gmail.com>

class Round(object):
    """ See Round.md for a complete guide to this class.
    """

    def __init__(self):
        self.players = []
        self.community_cards = []

    def add_player(self, player):
        self.players.append(player)

    def add_players(self, player_arr):
        for i in player_arr:
            self.players.append(i)


    # TODO - I'm not sure how to do the betting, gonna think about it for a while
    def bet(self):