from monte_carlo.components.models.Game import Game
from monte_carlo.components.models.Player import Player
import monte_carlo.components.managers.GameManager as gm
import monte_carlo.components.managers.PlayerManager as pm
import jsonpickle


game = Game()

a = Player("A", 10)
b = Player("B", 20)
c = Player("C", 20)


game.add_player(a)
game.add_player(b)
game.add_player(c)

game.start()
game.bm.startBettingRound()
print("First bettor = " + str(game.bm.nextBettor()))

game.bm.bet(a, 10, True)
print("Next bettor = " + str(game.bm.nextBettor()))

game.bm.bet(b, 15, True)
print("Next bettor = " + str(game.bm.nextBettor()))
# print("Bet Status: " + str(game.bm.getBetStatus()))
# print("Table: " + str([str(player) for player in game.bm.table]))
# d = {player.name: result for player, result in game.bm.}

game.bm.bet(c, 15, False)
print("Next bettor = " + str(game.bm.nextBettor()))


# e agora tudo tá funcionando :)




