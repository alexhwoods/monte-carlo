from components.models.Game import Game
from components.managers import PlayerManager   # PlayerManager is not a class!!!


games = {}
past_games = {}


def createGame():
    # TODO - eventually set this up to handle a table min
    game = Game()
    games[str(game.id)] = game
    return game


def getPlayers(gameID):
    if gameID in games.keys():
        game = games[gameID]
        return game.players
    else:
        return None


def getByID(gameID):
    if gameID in games.keys():
        return games[gameID]
    elif gameID in past_games.keys():
        return past_games[gameID]
    return None


def joinGame(playerID, gameID):
    player = PlayerManager.getByID(playerID)
    game = getByID(gameID)

    if game is not None and player is not None and player not in game.players:
        game.add_player(player)
        return game.players

    elif game is not None:
        return game.players

    else:
        return None


def endGame(gameID):
    game = getByID(gameID)
    if gameID in games.keys():
        del games[gameID]
        past_games[gameID] = game
        game.over = True
        return 'Success'
    else:
        return 'Failure'


def getStatus(gameID):
    game = getByID(gameID)
    if game is not None:
        status = str({player.name: player.chips for player in game.players})
        if game.started:
            status += ', was started. ' + str(len(game.rounds)) + ' rounds have occured.'
            if game.over: status += 'Game Over.'
        else: status += ', not started.'
    else:
        status = 'Game does not exist.'

    return status



