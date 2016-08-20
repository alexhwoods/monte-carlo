from monte_carlo import app
import monte_carlo.components.managers.GameManager as gm
import monte_carlo.components.managers.PlayerManager as pm

from monte_carlo.components.models.Deck import Deck
from flask import request
import jsonpickle

# TODO - make the urls better

@app.route('/test', methods=['GET'])
def test_method():
    return 'THIS IS A TEST'


@app.route('/advanced-test', methods=['GET'])
def advanced_test():
    deck = Deck()
    return jsonpickle.encode(deck)


@app.route('/game', methods=['POST'])
def create_game():
    gm.createGame()
    return 'Success'


@app.route('/games', methods=['GET'])
def get_games():
    return jsonpickle.encode(gm.games)


@app.route('/past-games', methods=['GET'])
def past_games():
    return jsonpickle.encode(gm.past_games)


# gets players for a given game
@app.route('/game/players', methods=['GET'])
def get_players():
    data = request.json
    gameID = data["gameID"]

    players = gm.getPlayers(gameID)
    return jsonpickle.encode(players)


@app.route('/games/find', methods=['GET'])
def get_game():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    game_json = jsonpickle.encode(game)
    return game_json


@app.route('/game', methods=['PUT'])
def joinGame():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    # message is 'Success' or 'Failure'...I just can't make myself JSON encode this
    message = gm.joinGame(playerID, gameID)
    return message


@app.route('/game/start', methods=['POST'])
def startGame():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    game.start()
    return 'Game Started'


# It's important to not create a new round if one is still going on!
@app.route('/game/round/new', methods=['POST'])
def newRound():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    game.newRound()
    return 'New Round Created'


@app.route('/game/end', methods=['POST'])
def endGame():
    data = request.json
    gameID = data["gameID"]

    message = gm.endGame(gameID)
    return message

@app.route('/game/winner', methods=['GET'])
def getGameWinner():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    return jsonpickle.encode(game.winner())


@app.route('/player/new', methods=['POST'])
def create_player():
    data = request.json
    name = data["name"]
    chips = data["chips"]
    player = pm.create(name, chips)
    return jsonpickle.encode(player)


@app.route('/game/round/deal', methods=['POST'])
def deal():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    round.deal()
    return round.stage + ' is dealt.'

# given a player ID and game ID return their hole cards for the current round
@app.route('/player/cards', methods=['GET'])
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


# given a game id get the community cards for the current round
@app.route('/game/cards', methods=['GET'])
def getCommunityCards():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    return jsonpickle.encode(round.community_cards)


# go to the next stage of a round
@app.route('/game/round/next', methods=['POST'])
def nextStage():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    round.next_stage()

    return jsonpickle.encode(round.stage)


@app.route('/game/over', methods=['GET'])
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


@app.route('/game/round/num', methods=['GET'])
def getRoundNumber():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(len(game.rounds))


# start betting round
@app.route('/game/round/end', methods=['POST'])
def startBettingRound():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    game.bm.startBettingRound()
    
    # I guess I'll return the first player to bet
    return jsonpickle.encode(game.bm.players[0])


@app.route('/game/round/betting/current', methods=['GET'])
def getCurrentBet():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(game.bm.current_bet)


@app.route('/game/round/betting/options', methods=['GET'])
def getBettingOptions():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    return jsonpickle.encode(game.bm.getOptions(player))


@app.route('/game/round/betting/limit', methods=['GET'])
def getRaiseLimit():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)

    return jsonpickle.encode(game.bm.getRaiseLimit(player))


@app.route('/game/round/fold', methods=['POST'])
def fold():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    
    game.bm.fold(player)
    return jsonpickle.encode(game.bm.getRaiseStatus())


@app.route('/game/round/bet', methods=['POST'])
def bet():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    
    amount = int(data['amount'])
    is_raise = bool(data['is_raise'])
    
    game.bm.bet(player, amount, is_raise)
    
    return jsonpickle.encode(game.bm.getRaiseStatus())


# these are the winners for the round, not the entire game. Will return None if round is still going.
@app.route('/game/round/winner', methods=['GET'])
def getRoundWinners():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(game.bm.getAllWinners())


# SUPER IMPORTANT METHOD RIGHT HERE!!! This determines if the betting round can stop or not.
@app.route('/game/round/status/raise', methods=['GET'])
def getRaiseStatus():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    return jsonpickle.encode(game.bm.getRaiseStatus())


@app.route('/game/round/status/fold', methods=['GET'])
def getFoldStatus():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    return jsonpickle.encode(game.bm.getFoldStatus())




