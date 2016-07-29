from monte_carlo.components.managers.Game import Game
from monte_carlo.components.models.Player import Player




""" Testing the get_winners() function in Round.py.

    Each time the following gets run, the deck is shuffled and new cards are dealt to each of the players.
"""

game2 = Game()
game2.add_player(Player("Silvia", 400))
game2.add_player(Player("Randolf", 400))

game2.test_winners()



# TODO
""" Testing the flow of a game

"""