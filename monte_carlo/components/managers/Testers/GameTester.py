from monte_carlo.components.managers.Game import Game
from monte_carlo.components.models.Player import Player

game = Game()
game.add_player(Player("Silvia", 400))
game.add_player(Player("Randolf", 400))


# If you uncomment this line, it will show just the functionality of deciding between hands
# game.test_winners()
game.run()


