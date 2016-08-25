from monte_carlo import app
import monte_carlo.components.managers.GameManager as gm
import monte_carlo.components.managers.PlayerManager as pm

from monte_carlo.components.models.Deck import Deck
from flask import request
import jsonpickle


''' Start server by typing 'sh bin/start_server.sh' in the main directory.

    TODO - make the urls better

    note - JSON strings must always use double quotes

'''

@app.route('/test', methods=['VIEW'])
def test_method():
    return 'THIS IS A TEST'


# tested
@app.route('/game', methods=['POST'])
def create_game():
    game = gm.createGame()
    return jsonpickle.encode(game)


# tested
@app.route('/games', methods=['VIEW'])
def get_games():
    return jsonpickle.encode(gm.games)


# tested
@app.route('/games/ids', methods=['VIEW'])
def get_gameIDs():
    return jsonpickle.encode(list(gm.games.keys()))


# not tested
@app.route('/past-games', methods=['VIEW'])
def past_games():
    return jsonpickle.encode(gm.past_games)


# tested - gets players for a given game
@app.route('/game/players', methods=['VIEW'])
def get_players():
    data = request.json
    gameID = data["gameID"]

    players = gm.getPlayers(gameID)
    return jsonpickle.encode(players)


# tested
@app.route('/games/find', methods=['VIEW'])
def get_game():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    return jsonpickle.encode(game)


# tested
@app.route('/game/join', methods=['POST'])
def joinGame():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]
    players = gm.joinGame(playerID, gameID)
    if players is not None:
        return jsonpickle.encode({gameID: [player.name for player in players]})
    else:
        return None


# tested
@app.route('/game/start', methods=['POST'])
def startGame():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    if game is not None:
        game.start()
    return gm.getStatus(gameID)


# tested
@app.route('/game/end', methods=['POST'])
def endGame():
    data = request.json
    gameID = data["gameID"]

    gm.endGame(gameID)
    return gm.getStatus(gameID)


@app.route('/game/winner', methods=['VIEW'])
def getGameWinner():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    return jsonpickle.encode(game.winner())


# tested
@app.route('/player/new', methods=['POST'])
def create_player():
    data = request.json
    name = data["name"]
    chips = data["chips"]
    player = pm.create(name, chips)
    return jsonpickle.encode(player)


# tested
@app.route('/players', methods=['VIEW'])
def get_all_players():
    return jsonpickle.encode(pm.players)


# tested
@app.route('/players/ids', methods=['VIEW'])
def get_all_player_ids():
    return jsonpickle.encode(list(pm.players.keys()))


@app.route('/game/round/deal', methods=['POST'])
def deal():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    round.deal()
    return round.stage + ' is dealt.'


# tested
# given a player ID and game ID return their hole cards for the current round
@app.route('/player/cards', methods=['VIEW'])
def getHoleCards():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)

    if player in game.players:
        return jsonpickle.encode(player.hand)
    else:
        return None


# tested
# given a game id get the community cards for the current round
@app.route('/game/cards', methods=['VIEW'])
def getCommunityCards():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    return jsonpickle.encode(round.community_cards)

# tested
# go to the next stage of a round
@app.route('/game/round/next', methods=['POST'])
def nextStage():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    round.next_stage()

    return jsonpickle.encode(round.stage)


@app.route('/game/over', methods=['VIEW'])
def gameIsOver():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(game.isOver())


@app.route('/game/round/end', methods=['POST'])
def endCurrentRound():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    game.endCurrentRound()
    return 'Round ended.'


# It's important to not create a new round if one is still going on!
@app.route('/game/round/new', methods=['POST'])
def newRound():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    val = game.newRound()
    if val:
        return 'New Round Created'
    else:
        return 'Still in previous round.'


@app.route('/game/round/num', methods=['VIEW'])
def getRoundNumber():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(len(game.rounds))


# tested
@app.route('/game/round/betting/start', methods=['POST'])
def startBettingRound():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    game.bm.startBettingRound()
    
    # I guess I'll return the first player to bet
    return jsonpickle.encode(game.bm.players[0])


# tested
@app.route('/game/round/betting/current', methods=['VIEW'])
def getCurrentBet():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(game.bm.current_bet)


# tested
@app.route('/game/round/betting/options', methods=['VIEW'])
def getBettingOptions():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    return jsonpickle.encode(game.bm.getOptions(player))


# tested
@app.route('/game/round/betting/limit', methods=['VIEW'])
def getRaiseLimit():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)

    return jsonpickle.encode(game.bm.getRaiseLimit(player))

# tested
@app.route('/game/round/fold', methods=['POST'])
def fold():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    
    game.bm.fold(player)
    return jsonpickle.encode(game.bm.nextBetter())


# some testing done
@app.route('/game/round/bet', methods=['POST'])
def bet():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    
    amount = int(data["amount"])
    is_raise = bool(data["is_raise"])
    
    game.bm.bet(player, amount, is_raise)
    
    return jsonpickle.encode(game.bm.nextBetter())


# TODO: TEST
@app.route('/game/round/pots', methods=['VIEW'])
def getPots():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    return jsonpickle.encode(game.bm.getPots())


# Seems to be working
@app.route('/game/round/betting/next', methods=['VIEW'])
def nextBetter():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    return jsonpickle.encode(game.bm.nextBetter())


# these are the winners for the round, not the entire game. Will return None if round is still going.
@app.route('/game/round/winner', methods=['VIEW'])
def getRoundWinners():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(game.bm.getAllWinners())


# TODO: test more, jsonpickle doesn't handle dictionaries well
@app.route('/game/round/status/raise', methods=['VIEW'])
def getRaiseStatus():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    return jsonpickle.encode(game.bm.getRaiseStatus())


# TODO: test more, jsonpickle doesn't handle dictionaries well
@app.route('/game/round/status/fold', methods=['VIEW'])
def getFoldStatus():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    return jsonpickle.encode(game.bm.getFoldStatus())




