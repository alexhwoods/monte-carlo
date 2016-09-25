from monte_carlo import app
import monte_carlo.components.managers.GameManager as gm
import monte_carlo.components.managers.PlayerManager as pm

from monte_carlo.components.models.Deck import Deck
from flask import request
import jsonpickle


''' Start server by typing 'sh bin/start_server.sh' in the main directory.

    Or just type 'mc', followed by 'mc-start' (only works on Alex's computer).

    TODO - make the urls bettor

    note - JSON strings must always use double quotes
    note - in JSON, send true as 1 and false as 0.

    note - an oddity of uuid, but when you return player.id, it returns a hash including dashes. However,
           when you return player, it doesn't have dashes. Wierd...

'''

# **************************************************** General ****************************************************

# tested TODO - check return val
@app.route('/games', methods=['GET', 'VIEW'])
def getGames():
    return jsonpickle.encode(gm.games)

# tested TODO - check return val
@app.route('/games/ids', methods=['GET', 'VIEW'])
def getGameIDs():
    dict = {}
    string = "game"
    num = 1
    for id in gm.games.keys():
        string += str(num) + "ID"
        num += 1
        dict[string] = id
        string = "game"

    return jsonpickle.encode(dict)

# not tested; TODO - check return val
@app.route('/games/past', methods=['GET', 'VIEW'])
def pastGames():
    return jsonpickle.encode(gm.past_games)



# tested - gets players for a given game; TODO - check return val
@app.route('/game/players', methods=['GET', 'VIEW'])
def getPlayers():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    # players = gm.getPlayers(gameID)
    ids = [str(player.id) for player in game.players]
    return jsonpickle.encode(ids)


# **************************************************** Game ****************************************************
# tested TODO - needs a better url
@app.route('/game/new', methods=['POST'])
def createGame():
    game = gm.createGame()

    # this dummy return val was here for testing
    # return jsonpickle.encode(game)
    
    return jsonpickle.encode(game.toSimple())


# tested
@app.route('/games/find', methods=['GET', 'VIEW'])
def getGame():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    return jsonpickle.encode(game.toSimple())

# return a full game, not just a simplified one
@app.route('/games/find/full', methods=['GET', 'VIEW'])
def getGameFull():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    return jsonpickle.encode(game)


# tested TODO - check return val
@app.route('/game/join', methods=['POST'])
def joinGame():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]
    players = gm.joinGame(playerID, gameID)
    if players is not None:
        return jsonpickle.encode({playerID: "Joined"})
    else:
        return jsonpickle.encode({playerID: "Not Found"})


# tested TODO - check return val
@app.route('/game/start', methods=['POST'])
def startGame():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    if game is not None:
        game.start()
        return jsonpickle.encode({gameID: "Started"})
    else:
        return jsonpickle.encode({gameID: "Not Found"})


# tested TODO - check return val 
@app.route('/game/end', methods=['POST'])
def endGame():
    data = request.json
    gameID = data["gameID"]

    gm.endGame(gameID)
    return gm.getStatus(gameID)

# TODO - check return val
@app.route('/game/winner', methods=['GET', 'VIEW'])
def getGameWinner():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    winner = game.winner()
    return jsonpickle.encode(str(winner.id))


# **************************************************** Player ****************************************************
# tested
@app.route('/player/new', methods=['POST'])
def createPlayer():
    data = request.json
    name = data["name"]
    chips = data["chips"]
    player = pm.create(name, chips)
    return jsonpickle.encode({"id": str(player.id)})


# tested TODO - make it return player's ID
@app.route('/players', methods=['GET', 'VIEW'])
def getAllPlayers():
    return jsonpickle.encode(pm.players)


# tested TODO - is this returning ID's
@app.route('/players/ids', methods=['GET', 'VIEW'])
def getAllPlayerIds():
    dict = {}
    string = "player"
    num = 1
    for id in pm.players.keys():
        string += str(num) + "ID"
        num += 1
        dict[string] = id

        string = "player"

    d = {pm.players[id].name: id for id in pm.players.keys()}

    return jsonpickle.encode(d)


# ************************************************ Dealing **********************************************************
# TODO - is this the return value you want?
@app.route('/game/round/deal', methods=['POST'])
def deal():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    if game is None:
    	print("Game is none..hmmm")
    round = game.getCurrentRound()
    previous_stage = round.stage
    round.deal()

    d = {"Previous Stage": previous_stage,
         "Current Stage": round.stage}

    return jsonpickle.encode(d)


# tested TODO - edit return value
# given a player ID and game ID return their hole cards for the current round
@app.route('/player/cards', methods=['GET', 'VIEW'])
def getHoleCards():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)

    if player in game.players:
        arr = [str(card) for card in player.hand]
        return jsonpickle.encode(arr)

        # I'll return this one later, when I actually need to do stuff with the request
        # return jsonpickle.encode(player.hand)
    else:
        return "Player Not Found"


# tested TODO - edit return value
# given a game id get the community cards for the current round
@app.route('/game/cards', methods=['GET', 'VIEW'])
def getCommunityCards():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    round = game.getCurrentRound()

    arr = [str(card) for card in round.community_cards]
    return jsonpickle.encode(arr)

    # return jsonpickle.encode(round.community_cards)

# TODO - edit return value
@app.route('/game/over', methods=['GET', 'VIEW'])
def gameIsOver():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(game.isOver())

# This method is just to make testing easier, TODO - edit return value
@app.route('/game/card/status', methods=['GET', 'VIEW'])
def cardStatus():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    commCards = [str(card) for card in round.community_cards]

    playerCards = {player.name: [str(card) for card in player.hand] for player in game.players}
    playerFold = [player.name for player in game.players if player.folded]

    d = {"Community Cards": commCards, "Player's Hands": playerCards, 
        "Players who've folded": playerFold}

    return jsonpickle.encode(d)


# ************************************************ Round **************************************************************
# tested TODO - check return val
@app.route('/game/round/end', methods=['POST'])
def endCurrentRound():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    game.endCurrentRound()
    chips = {player.name: player.chips for player in game.players}

    return jsonpickle.encode(chips)


# It's important to not create a new round if one is still going on!
# TODO - check return val
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

# TODO - check return val
@app.route('/game/round/num', methods=['GET', 'VIEW'])
def getRoundNumber():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(len(game.rounds))

# TODO - check return val
# these are the winners for the round, not the entire game. Will return None if round is still going.
@app.route('/game/round/winner', methods=['GET', 'VIEW'])
def getRoundWinners():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode(game.bm.getAllWinners())


# ************************************************ Betting ***********************************************************
# tested TODO - check return val
@app.route('/game/round/betting/start', methods=['POST'])
def startBettingRound():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    firstOfRound = bool(data["firstOfRound"])
    game.bm.startBettingRound(firstOfRound)

    next_bettor = game.bm.nextBettor()

    if next_bettor is not None:
        return jsonpickle.encode({"playerID": str(next_bettor.id)})
    else:
        return "Game has no players."

# tested TODO - check return val
@app.route('/game/round/betting/current', methods=['GET', 'VIEW'])
def getCurrentBet():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return jsonpickle.encode({"currentBet": game.bm.current_bet})


# tested TODO - check return val
@app.route('/game/round/betting/options', methods=['GET', 'VIEW'])
def getBettingOptions():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    return jsonpickle.encode(game.bm.getOptions(player))

# TODO - check return val
@app.route('/game/status/bet', methods=['GET', 'VIEW'])
def getBetStatus():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]
    per_betting_round = bool(data["per_betting_round"])

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    dict = game.bm.getBetStatus(per_betting_round)

    if player in dict.keys():
        return jsonpickle.encode({"playerID": str(player.id), "amount": dict[player]})
    else:
        return "Player not in summary for some reason"


# more for testing than for use TODO - check return val
@app.route('/game/status/chips', methods=['GET', 'VIEW'])
def getChipStatus():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    
    d = {str(player.name): game.bm.chips[player] for player in game.bm.players}
    return jsonpickle.encode(d)


# TODO - check return val
@app.route('/game/status/bets/all', methods=['GET', 'VIEW'])
def getBetStatusAll():
    data = request.json
    gameID = data["gameID"]
    per_betting_round = bool(data["per_betting_round"])

    game = gm.getByID(gameID)
    # players = gm.getPlayers(gameID)
    dict = game.bm.getBetStatus(per_betting_round)

    return jsonpickle.encode({str(player.id): dict[player] for player in dict.keys()})



# tested TODO - check return val
@app.route('/game/round/betting/limit', methods=['GET', 'VIEW'])
def getRaiseLimit():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)

    return jsonpickle.encode(game.bm.getRaiseLimit(player))

# tested TODO - check return val
@app.route('/game/round/fold', methods=['POST'])
def fold():
    data = request.json
    gameID = data["gameID"]
    playerID = data["playerID"]

    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    
    game.bm.fold(player)

    next_bettor = game.bm.nextBettor()

    if next_bettor is not None:
        return jsonpickle.encode({"playerID": str(next_bettor.id)})
    else:
        return "null"


# tested TODO - check return val
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

    next_bettor = game.bm.nextBettor()

    if next_bettor is not None:
        return jsonpickle.encode({"playerID": str(next_bettor.id)})
    else:
        return "null"

# TODO - check return val; TODO - is this tested?
@app.route('/game/round/pots', methods=['GET', 'VIEW'])
def getPots():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    return jsonpickle.encode(game.bm.getPots())


# tested TODO - check return val
@app.route('/game/round/betting/next', methods=['GET', 'VIEW'])
def nextBettor():
    data = request.json
    gameID = data["gameID"]

    game = gm.getByID(gameID)
    next_bettor = game.bm.nextBettor()

    if next_bettor is not None:
        return jsonpickle.encode({"playerID": str(next_bettor.id)})
    else:
        return "null"


# tested TODO - check return val
@app.route('/game/round/status/raise', methods=['GET', 'VIEW'])
def getRaiseStatus():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    # return jsonpickle.encode(game.bm.getRaiseStatus())

    d = game.bm.getRaiseStatus()
    temp = {str(player.id): d[player] for player in d.keys()}
    return jsonpickle.encode(temp)


# tested TODO - check return val
@app.route('/game/round/status/fold', methods=['GET', 'VIEW'])
def getFoldStatus():
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    dict = game.bm.getFoldStatus()
    dict2 = {str(player.id): str(dict[player]) for player in dict.keys()}

    dict3 = {player.name: str(dict[player]) for player in dict.keys()}

    return jsonpickle.encode(dict3)




