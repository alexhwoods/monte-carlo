from monte_carlo import app
from monte_carlo.components.models.Game import Game
import monte_carlo.components.managers.GameManager as gm
import monte_carlo.components.managers.PlayerManager as pm

# TODO - all necessary parameters in each method need to be grabbed through JSON

@app.route('/test', methods=['GET'])
def test_method():
    return 'THIS IS A TEST'


@app.route('/game', methods=['POST'])
def create_game():
    game = gm.createGame()
    return game


# gets players for a given game
@app.route('/game/players', methods=['GET'])
def get_players():
    gameID = 1234
    players = gm.getPlayers(gameID)
    return players


@app.route('/games/find', methods=['GET'])
def get_game():
    gameID = 1234
    game = gm.getByID(gameID)
    return game


@app.route('/game', methods=['PUT'])
def joinGame():
    gameID = 1234
    playerID = 5678

    # message is 'Success' or 'Failure'
    message = gm.joinGame(playerID, gameID)
    return message


@app.route('game/start', methods=['POST'])
def startGame():
    gameID = 1234
    game = gm.getByID(gameID)
    game.start()
    return 'Game Started'


# It's important to not create a new round if one is still going on!
@app.route('game/round/new', methods=['POST'])
def newRound():
    gameID = 1234
    game = gm.getByID(gameID)
    game.newRound()
    return 'New Round Created'


@app.route('/game/end', methods=['POST'])
def endGame():
    gameID = 1234

    message = gm.endGame(gameID)
    return message

@app.route('/game/winner', methods=['GET'])
def getGameWinner():
    gameID = 1234
    game = gm.getByID(gameID)
    return game.winner()


@app.route('/player/new', methods=['POST'])
def create_player():
    name = 'John Doe'
    chips = 100
    player = pm.create(name, chips)
    return player


@app.route('/game/round/deal', methods=['POST'])
def deal():
    gameID = 1234
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    round.deal()
    return round.stage + ' is dealt.'

# given a player ID and game ID return their hole cards for the current round
@app.route('/player/cards', methods=['GET'])
def getHoleCards():
    gameID = 1234
    game = gm.getByID(gameID)

    playerID = 5678
    player = pm.getByID(playerID)

    if player in game.players:
        return player.hand
    else:
        return None


# given a game id get the community cards for the current round
@app.route('/game/cards', methods=['GET'])
def getCommunityCards():
    gameID = 1234
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    return round.community_cards


# go to the next stage of a round
@app.route('game/round/next', methods=['POST'])
def nextStage():
    gameID = 1234
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    round.next_stage()

    return round.stage


@app.route('game/over', methods=['GET'])
def gameIsOver():
    gameID = 1234
    game = gm.getByID(gameID)
    return game.isOver()


@app.route('game/round/end', methods=['POST'])
def endCurrentRound():
    gameID = 1234
    game = gm.getByID(gameID)
    game.endCurrentRound()


@app.route('game/round/num', methods=['GET'])
def getRoundNumber():
    gameID = 1234
    game = gm.getByID(gameID)

    return len(game.rounds)


# start betting round
@app.route('game/round/end', methods=['POST'])
def startBettingRound():
    gameID = 1234
    game = gm.getByID(gameID)
    game.bm.startBettingRound()
    
    # I guess I'll return the first player to bet
    return game.bm.players[0]


@app.route('game/round/betting/current', methods=['GET'])
def getCurrentBet():
    gameID = 1234
    game = gm.getByID(gameID)
    return game.bm.current_bet


@app.route('game/round/betting/options', methods=['GET'])
def getBettingOptions():
    gameID = 1234
    game = gm.getByID(gameID)

    playerID = 5678
    player = pm.getByID(playerID)
    return game.bm.getOptions(player)


@app.route('game/round/betting/limit', methods=['GET'])
def getRaiseLimit():
    gameID = 1234
    game = gm.getByID(gameID)

    playerID = 5678
    player = pm.getByID(playerID)
    
    return game.bm.getRaiseLimit(player)


@app.route('game/round/fold', methods=['POST'])
def fold():
    gameID = 1234
    game = gm.getByID(gameID)

    playerID = 5678
    player = pm.getByID(playerID)
    
    game.bm.fold(player)
    return game.bm.getRaiseStatus()


@app.route('game/round/bet', methods=['POST'])
def bet():
    gameID = 1234
    game = gm.getByID(gameID)

    playerID = 5678
    player = pm.getByID(playerID)
    
    amount = 45
    is_raise = False
    
    game.bm.bet(player, amount, is_raise)
    
    return game.bm.getRaiseStatus()


# these are the winners for the round, not the entire game. Will return None if round is still going.
@app.route('game/round/winner', methods=['GET'])
def getRoundWinners():
    gameID = 1234
    game = gm.getByID(gameID)

    return game.bm.getAllWinners()


# SUPER IMPORTANT METHOD RIGHT HERE!!! This determines if the betting round can stop or not.
@app.route('game/round/status/raise', methods=['GET'])
def getRaiseStatus():
    gameID = 1234
    game = gm.getByID(gameID)
    return game.bm.getRaiseStatus()


@app.route('game/round/status/fold', methods=['GET'])
def getFoldStatus():
    gameID = 1234
    game = gm.getByID(gameID)
    return game.bm.getFoldStatus()




