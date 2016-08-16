from monte_carlo.components.managers.BetManager import BetManager
from monte_carlo.components.models.Game import Game
from monte_carlo.components.models.Player import Player
from monte_carlo.components.models.Round import Round

A = Player("A", 300)
B = Player("B", 200)
C = Player("C", 100)
# D = Player("D", 400)
players_dict = {A: A.chips, B: B.chips, C: C.chips}

game = Game()
# can't handle a game with no players even though I'm just testing...
game.add_player(A)
game.add_player(B)
game.add_player(C)
# game.add_player(D)
round = Round(game)
casino = BetManager(round)

# bets = {A: 250, B: 200, C: 100, D: 20}  # check
bets = {A: 240, B: 0, C: 0}  # check
# bets = {A: 250, B: 250, C: 100, D: 20}  # check
# bets = {A: 242, B: 250, C: 350, D: 20}  # check

casino.bet_tester(players_dict, bets)

