from monte_carlo.components.models.Game import Game
from monte_carlo.components.models.Player import Player
import monte_carlo.components.managers.PlayerManager as pm


games = []
past_games = []


def createGame():
    # TODO - eventually set this up to handle a table min
    game = Game()
    games.append(game)


def getPlayers(gameID):
    for game in games:
        if game.id == gameID:
            return game.players
    return None


def getByID(gameID):
    for game in games:
        if game.id == gameID:
            return game
    return None


def joinGame(playerID, gameID):
    player = pm.getByID(playerID)
    game = getByID(gameID)

    if game is not None and player is not None:
        game.add_player(player)
        return "Success"

    else:
        return "Failure"


def endGame(gameID):
    game = getByID(gameID)
    games.remove(game)
    past_games.append(game)



