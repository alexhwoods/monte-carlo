from monte_carlo.components.managers.Game import Game
from monte_carlo.components.models.Player import Player

game = Game()
game.add_player(Player("Silvia", 300))
game.add_player(Player("Randolf", 200))
game.add_player(Player("Germaine", 100))
# game.add_player(Player("Silvia", 300))
# game.add_player(Player("Randolf", 300))
# game.add_player(Player("Germaine", 300))


# If you uncomment this line, it will show just the functionality of deciding between hands
# game.test_winners()
game.test_betting()
# game.run()


