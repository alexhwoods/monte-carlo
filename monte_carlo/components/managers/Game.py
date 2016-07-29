# Author Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Deck import Deck
from monte_carlo.components.models.Player import Player
from monte_carlo.components.managers.Round import Round
from pprint import pprint

class Game(object):

    def __init__(self, table_min=0):
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

    def start_round(self):
        self.deck.shuffle()
        self.round = Round(self.deck, self.get_players(), self.table_min)
        self.round_num += 1

    def execute_round(self):
        self.round.deal_hole()
        self.round.pre_flop()
        self.round.flop()
        self.round.post_flop()
        self.round.turn()
        self.round.post_turn()
        self.round.river()
        self.round.showdown()

        if self.round.over:
            winners = self.round.get_winner()
            print("The winner of the round is " + str([str(player) for player in winners[0]]))
            print("Their hands were:")
            pprint(winners[1])
            print("They won " + str(self.round.pot))

            to_recieve_chips = [player for player in winners[0]]
            if len(winners) == 1:
                to_recieve_chips[0].win(self.round.pot)

            # if there was a tie and the pot needs to be split among the winners
            else:
                share = self.round.pot / len(winners)
                for player in to_recieve_chips:
                    player.win(share)

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

    def test_winners(self):
        self.deck.shuffle()
        self.round = Round(self.deck, self.get_players(), self.table_min)
        self.round.deal_hole()
        self.round.flop()
        self.round.turn()
        self.round.river()
        print("\n")
        self.round.over = True
        self.round.show_all()
        if self.round.over:
            winners = self.round.get_winner()
            print("The winner of the round is " + str([str(player) for player in winners[0]]))
            print("Their hands were:")
            pprint(winners[1])
            print("They won " + str(self.round.pot))

            to_receive_chips = [player for player in winners[0]]
            if len(winners) == 1:
                to_receive_chips[0].win(self.round.pot)

            # if there was a tie and the pot needs to be split among the winners
            else:
                share = self.round.pot / len(winners)
                for player in to_receive_chips:
                    player.win(share)

    def show(self):
        arr = []
        for i in self.players:
            arr.append(str(i))
        pprint(arr)
        print("The minimum table bet is " + str(self.table_min) + " chips.")
        print("\n")
        if self.round is not None:
            self.round.show_all()



# Testing Session 1

# game = Game()
# carla = Player("Carla", 200)
# game.add_player(carla)
#
# bob = Player("Bob", 350)
# game.add_player(Player("Bob", 350))
#
# carlos = Player("Carlos", 300)
# game.add_player(carlos)
#
# game.show()
# game.start_round()
# game.execute_round()
# game.end_round()

# Testing Session 2 - testing the get_winners() function in round. See GameTester.py
game2 = Game()
game2.add_player(Player("Silvia", 400))
game2.add_player(Player("Randolf", 400))

game2.test_winners()


