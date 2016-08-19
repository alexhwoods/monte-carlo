from monte_carlo.components.models.Game import Game
from monte_carlo.components.models.Player import Player
import monte_carlo.components.managers.PlayerManager as pm


games = {}
past_games = {}


def createGame():
    # TODO - eventually set this up to handle a table min
    game = Game()
    games[game.id] = game
    return game


def getPlayers(gameID):
    for game in games:
        if game.id == gameID:
            return game.players
    return None


def getByID(gameID):
    if gameID in games.keys():
        return games[gameID]
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
    if game in games:
        del games[gameID]
        past_games[gameID] = game
        return 'Success'
    else:
        return 'Failure'



