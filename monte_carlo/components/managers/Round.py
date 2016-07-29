# Author Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Deck import Deck
from monte_carlo.components.models.Player import Player
from monte_carlo.components.models.Hand import Hand
from monte_carlo.components.models.Card import Card
from itertools import combinations

from pprint import pprint

class Round(object):
    """ See Round.md for a complete guide to this class.
    """

    def __init__(self, deck, players=[], min_bet=10):
        self.players = players
        self.deck = deck
        self.community_cards = []
        self.table_min_bet = min_bet
        self.stage_min_bet = min_bet
        self.stage = None
        self.pot = 0
        self.over = False
        self.starting_chips = {player: player.chips for player in self.players}

    def add_player(self, player):
        self.players.append(player)

    def add_players(self, player_arr):
        for i in player_arr:
            self.players.append(i)

    def start_stage(self, stage):
        stages = ['PRE_FLOP', 'POST_FLOP', 'POST_TURN', 'SHOWDOWN']
        if stage.upper() in stages:
            self.stage = stage.upper()
            print("We are now in the " + str(self.stage) + " stage.")



    # Below are functions related to the dealing of cards

    def deal_hole(self):
        for player in self.players:
            player.set_hand(self.deck.draw_many(2))

    def flop(self):
        self.community_cards = self.deck.draw_many(3)
        # print("The table cards are:")
        self.cards_print = [str(card) for card in self.community_cards]
        # pprint(self.cards_print)

    def turn(self):
        turn = self.deck.draw_one()
        self.community_cards.append(turn)
        self.cards_print.append(str(turn))

        # print("\n The table cards are:")
        # pprint(self.cards_print)

    def river(self):
        river = self.deck.draw_one()
        self.community_cards.append(river)
        self.cards_print.append(str(river))

        # all the players calculate their best hand
        for player in self.players:
            player.best_round_hand = Hand.get_best_hand(self.community_cards + player.hand.cards)

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

    # only access betting through this function, better for game flow
    def bet(self, player, amount):
        if amount >= self.stage_min_bet and not player.folded:
            player.bet(amount)

            self.stage_min_bet = amount
            self.pot += amount
        else:
            pass

    def pre_flop(self):
        self.start_stage('PRE_FLOP')
        self.stage_min_bet = self.table_min_bet
        self.prompt_to_bet()

    def post_flop(self):
        self.start_stage('POST_FLOP')
        self.stage_min_bet = self.table_min_bet
        self.prompt_to_bet()

    def post_turn(self):
        self.start_stage('POST_TURN')
        self.stage_min_bet = self.table_min_bet
        self.prompt_to_bet()

    def showdown(self):
        self.start_stage('SHOWDOWN')
        self.stage_min_bet = self.table_min_bet
        self.prompt_to_bet()

        self.over = True

    def prompt_to_bet(self):
        print("Enter 0 to bet nothing, and 999 to fold. \n")
        bets = {}
        for player in self.players:
            if not player.folded:
                bet_amount = -100
                print("Hi " + str(player.name) + ". Your cards are ")
                player.hand.show()
                while bet_amount < self.stage_min_bet or bet_amount > player.chips:
                    bet_amount = int(input("Your bet must be at least " + str(self.stage_min_bet) +
                                           ". Enter an amount:"))
                    bets[player] = bet_amount
                    if bet_amount == 999:
                        player.fold()
                        break

                    bet_amount = min(bet_amount, min([chips for player, chips in self.starting_chips.items() if not player.folded]))
                self.bet(player, bet_amount)
                print("\n")

        # if a player raises, the previous players have to choose to match it or to fold
        bets = {key: value for key, value in bets.items() if value != 999}
        bets_display = {key.name: value for key, value in bets.items()}
        print("bets:")
        pprint(bets_display)

        # Looping through the players who haven't matched the max bet
        for player in [key for key, value in bets.items() if value != max(bets.values())]:
            text = ''
            print("Type yes or no")
            while text.upper() not in ['YES', 'NO']:
                text = input(player.name + ", would you like to match the highest bet of "
                             + str(max(bets.values())) + ":")

            if text.upper() == 'YES':
                self.bet(player, max(bets.values()) - bets[player])
            else:
                player.fold()

        print("\n")

    def get_winner(self):
        for player in self.players:
            player.best_round_hand = Hand.get_best_hand(self.community_cards + player.hand.cards)

        winners = [self.players[0]]
        best_hand = winners[0].best_round_hand
        for player in self.players:
            if Hand.winner(best_hand, player.best_round_hand) == player.best_round_hand:
                # if there is a clear winner we need to reset the winners array, because maybe there was a tie
                # between two players and a third player beat one of them (and thus both of them)
                winners = [player]
                best_hand = player.best_round_hand

            # if there is a tie!
            elif Hand.winner(best_hand, player.best_round_hand) is None and player not in winners:
                winners.append(player)
            else:
                pass

        return winners

    def end(self):
        self.pot = 0
        self.community_cards = []


    def show(self):
        arr = []
        for i in self.players:
            arr.append(str(i))
        pprint(arr)
        print("\n")
        print("Round is currently in " + str(self.stage) + " stage.")
        print("There is " + str(self.pot) + " in the pot.")

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
        print("Round is currently in " + str(self.stage) + " stage.")
        print("There is " + str(self.pot) + " in the pot. \n")
        print("The following players have folded:")
        pprint(out)


