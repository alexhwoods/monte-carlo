# Author Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Hand import Hand
from monte_carlo.components.managers.BetManager import BetManager

from pprint import pprint

class Round(object):
    """ See Round.md for a complete guide to this class.
    """

    def __init__(self, game):
        self.players = game.players
        self.deck = game.deck
        self.community_cards = []
        self.table_min = game.table_min
        self.bet_manager = BetManager(self)

        self.over = False
        self.winners = None


    def add_player(self, player):
        self.players.append(player)

    def add_players(self, player_arr):
        for i in player_arr:
            self.players.append(i)

    def start_stage(self, stage):
        stages = ['PRE_FLOP', 'POST_FLOP', 'POST_TURN', 'SHOWDOWN']
        if stage.upper() in stages:
            self.stage = stage.upper()
            print("stage: " + str(self.stage))



    # Below are functions related to the dealing of cards

    def deal_hole(self):
        for player in self.players:
            player.set_hand(self.deck.draw_many(2))

    def flop(self):
        self.community_cards = self.deck.draw_many(3)
        # print("The table cards are:")
        self.cards_print = [str(card) for card in self.community_cards]
        pprint(self.cards_print)

    def turn(self):
        turn = self.deck.draw_one()
        self.community_cards.append(turn)
        self.cards_print.append(str(turn))

        # print("\n The table cards are:")
        pprint(self.cards_print)

    def river(self):
        river = self.deck.draw_one()
        self.community_cards.append(river)
        self.cards_print.append(str(river))

        # all the players calculate their best hand
        for player in self.players:
            player.best_hand = Hand.get_best_hand(Hand(self.community_cards) + player.hand)

        print("\n The table cards are:")
        pprint(self.cards_print)



    """" Below are functions related to betting. There are 4 betting rounds:
        The pre-flop: the players have their two hole cards, but nothing else
        The post-flop: the players have their two hole cards, and can also
                       see 3 community cards.
        The post-turn: They can now see an additional community card.
        The showdown: They can see all 5 community cards. After this the round
                      is complete.
    """""

    def pre_flop(self):
        self.start_stage('PRE_FLOP')
        self.bet_manager.cl_betting_round(preflop=True)
        self.bet_manager.current_bet = 0

    def post_flop(self):
        if self.bet_manager.done_by_fold(): pass
        self.start_stage('POST_FLOP')
        self.bet_manager.cl_betting_round()
        self.bet_manager.current_bet = 0

    def post_turn(self):
        if self.bet_manager.done_by_fold(): pass
        self.start_stage('POST_TURN')
        self.bet_manager.cl_betting_round()
        self.bet_manager.current_bet = 0

    def showdown(self):
        if self.bet_manager.done_by_fold(): pass
        self.start_stage('SHOWDOWN')
        self.bet_manager.cl_betting_round()
        self.bet_manager.distribute()
        self.bet_manager.current_bet = 0

        self.over = True

    # def get_winner(self):
    #     # if all the players fold, we don't need to compare cards to see who wins, we just pick the one who
    #     # hasn't folded yet.
    #     if self.bet_manager.done_by_fold():
    #         for player in self.players:
    #             if not player.folded:
    #                 return [player]
    #
    #     for player in self.players:
    #         player.best_hand = Hand.get_best_hand(Hand(self.community_cards) + player.hand)
    #
    #     winners = [self.players[0]]
    #     best_hand = winners[0].best_hand
    #     for player in self.players:
    #         if Hand.winner(best_hand, player.best_hand) == player.best_hand:
    #             # if there is a clear winner we need to reset the winners array, because maybe there was a tie
    #             # between two players and a third player beat one of them (and thus both of them)
    #             winners = [player]
    #             best_hand = player.best_hand
    #
    #         # if there is a tie!
    #         elif Hand.winner(best_hand, player.best_hand) is None and player not in winners:
    #             winners.append(player)
    #         else:
    #             pass
    #
    #     self.winners = winners
    #     return winners

    def end(self):
        self.bet_manager.reset()
        self.community_cards = []

    def show(self):
        arr = []
        for i in self.players:
            arr.append(str(i))
        pprint(arr)

    def show_all(self):
        arr = []
        out = []
        for player in self.players:
            if not player.folded:
                print(str(player) + "\n current hand: \n")
                player.hand.show()
            else:
                out.append(str(player))
        print("\n")
        print("The following players have folded:")
        pprint(out)


