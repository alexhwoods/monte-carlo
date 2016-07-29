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
        print("The table cards are:")
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

    # get winner
    """"" This method is complicated because breaking a tie is complicated. 80% of the time
    there won't be a tie, and it's easy. However, we have to consider the case where people have
    very similar hands. There are legitimate situations that can end in a tie
    (i.e. community cards are a royal flush and both players hold a pair of 5's)

    1.  Some initialization. I'm going to set winners equal to all the players and then
        whittle it down to those with the best hands (and those not folded).

    2.  This block takes the hand that the winners are tied on, and puts it in a disabled list,
        so that way when block 3 searches for the next best hand, the previous hand is not considered.
        If it's a high card and they still tie, that means they really are tied.

    3. Loops all possible 5 cards hands of the 7 cards the player can use (2 hole cards and
       5 community cards). It assigns the player a score for their hand, and then the winners
       are selected based on that score. If there is a tie, we loop through again, except now
       the best hand that the tied players had is disabled, so it finds their next best hand.

    4. If everyone's best hand is a high card, we have to get the value of each players highest
       card, and score them on that.

    """""
    # TODO this method is not good enough. I need to fix it, with a rulebook by my right next to me as I do it.
    def get_winner(self):
        # 1
        hands = {}
        winners = self.players
        start = True
        highcard = False
        disabled = []
        while (len(winners) > 1 or start) and not highcard:

            # 2
            if len(winners) > 1 and not start:
                disabled.append(hands[winners[0]])

            # the first time through is pretty unique
            start = False

            # 3
            for player in winners:
                if not player.folded:
                    cards = player.hand.cards + self.community_cards
                    best_hand = 'HIGH_CARD'  # this is like setting max = 0 and then updating it


                    for combo in list(combinations(cards, 5)):
                        hand = Hand(list(combo))
                        if Hand.value[hand.type(disabled)] > Hand.value[best_hand]:
                            best_hand = hand.type(disabled)

                    hands[player] = best_hand

                else:
                    pass

            scores = {key: Hand.value[value] for key, value in hands.items()}
            scores_display = {str(player): value for player, value in scores.items()}
            pprint(scores_display)
            winners = [key for key, value in scores.items() if value == max(scores.values())]
            print("The winners pre-highcard are:")
            for x in winners: print(x.name)
            # 4. (if everyone's best unique hand is a high card)
            if set([hands[winner] for winner in winners]) == {'HIGH_CARD'}:
                print("Reached highcard")
                for player in winners:
                    # we only check the two hole cards for a high card
                    hand = player.hand.cards
                    scores[player] = max([Card.value[x.get_rank()] for x in hand])
                winners = [key for key, value in scores.items() if value == max(scores.values())]
                highcard = True

        # returns the winners as well as the winning hands
        return [winners, [hands[winner] for winner in winners]]

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


