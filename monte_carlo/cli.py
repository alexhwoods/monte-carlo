from components.managers import GameManager as gm
from components.managers import PlayerManager as pm
from components.models import Deck



''' This is the Command Line Interface for Monte Carlo.

	My goals with it are:

	1. Make it easy for a user to play a game.
	2. To keep things simple, a game will only be played user vs. AI.
	3. I would like to make it easy for a user to put a game on pause and come back later
	   (This means not having the program running while on pause!)

	note - make a JSON file with the default settings for some player.

	i.e. Their player ID, number of games played - that could be the new "game manager" or
	"player manager" for them. 

	At some point though their needs to be a database.

	note - make sure throughout the lifetime of the app that the user and the AI player
	have the same player ID.

	remember - bad requests break things!

	note - this is HELPER methods. In some cases, it's just easier to go directly
		   to the classes. Sometimes it's easier to go through here, but other cases no.
		   I'll comment by case
	

	There are a lot of things I'll have to edit once I have a better idea of design.
'''

# **************************************************** General ****************************************************
# what should a new game create? For now, I won't save old games. 
# I'll come back and do that when I write the ml part.

# todo
def reset():
    pass
	# make a new user player ID
	# make a new AI player ID
	# reset settings in JSON settings file


# **************************************************** Game ****************************************************
def createGame():
    game = gm.createGame()
    return game


# tested
def getGame(gameID):
    game = gm.getByID(gameID)
    return game



def joinGame(gameID, playerID):
	# just use game.add_player(player)
	pass
    


# note - does this make sense as a command line interface game? 
# TODO - redesign when you design the game flow
def startGame(gameID):
    game = gm.getByID(gameID)

    if game is not None:
        game.start()
        return True
    else:
        return False


def endGame(gameID):
    gm.endGame(gameID)
    return gm.getStatus(gameID)

def gameIsOver(gameID):
    game = gm.getByID(gameID)
    return game.isOver()

# TODO - check return val
def getGameWinner(gameID):
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)
    winner = game.winner()
    return str(winner.id)


# **************************************************** Player ****************************************************
# tested
def createPlayer(name, chips):
    player = pm.create(name, chips)
    return player


# note - useless
def getAllPlayers():
    return pm.players


# note - the player manager will be useless, the game manager maybe not
# TODO - delete or nah?
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

    return d

# TODO
def getPlayerIDs():
    pass
	# return the user's ID and the AI's ID
	# use the above method for inspiration
	# but get rid of player manager


# ************************************************ Dealing **********************************************************
def deal(gameID):
    game = gm.getByID(gameID)
    # if game is None:
    # 	print("Game is none..hmmm")
    round = game.getCurrentRound()
    previous_stage = round.stage
    round.deal()

    d = {"Stage Dealt": previous_stage,
         "Next Stage": round.stage}

    return d



# given a player ID and game ID return their hole cards for the current round
def getHoleCards(gameID, playerID):
    game = gm.getByID(gameID)
    player = pm.getByID(playerID)

    if player in game.players:
        return player.hand
    else:
        return None


# given a game id get the community cards for the current round
def getCommunityCards(gameID):
    game = gm.getByID(gameID)
    round = game.getCurrentRound()
    
    return round.community_cards


# note - THIS HAS BEEN SO HELPFUL IN TESTING
def cardStatus(gameID):
    game = gm.getByID(gameID)

    round = game.getCurrentRound()
    commCards = [str(card) for card in round.community_cards]

    playerCards = {player.name: [str(card) for card in player.hand] for player in game.players}
    playerFold = [player.name for player in game.players if player.folded]

    d = {"Community Cards": commCards, "Player's Hands": playerCards, 
        "Players who've folded": playerFold}

    return d


# ************************************************ Round **************************************************************
def endCurrentRound(gameID):
    game = gm.getByID(gameID)
    game.endCurrentRound()


# It's important to not create a new round if one is still going on!
def newRound(gameID):
    game = gm.getByID(gameID)
    val = game.newRound()

    # note - I'll leave this for now, but get rid of it
    if val:
        return {gameID: "round created"}
    else:
        return {gameID: "still in previous round"}


def getRoundNumber(gameID):
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return len(game.rounds)

# TODO - needs to be tested, just hard to test because it requires so much to be done before it is tested
# these are the winners for the round, not the entire game. Will return None if round is still going.
def getRoundWinners(gameID):
    data = request.json
    gameID = data["gameID"]
    game = gm.getByID(gameID)

    return game.bm.getAllWinners()


# ************************************************ Betting ***********************************************************
# tested 
def startBettingRound(gameID, firstOfRound=False):
    game = gm.getByID(gameID)
    game.bm.startBettingRound(firstOfRound)
    return game.bm.nextBettor()

# tested 
def getCurrentBet(gameID):
    game = gm.getByID(gameID)
    return game.bm.current_bet


# tested 
def getBettingOptions(gameID, playerID):
    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    return game.bm.getOptions(player)


def getBetStatus(gameID, playerID, perBettingRound=False):
    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    dict = game.bm.getBetStatus(perBettingRound)

    if player in dict.keys():
        return {"playerID": str(player.id), "amount": dict[player]}
    else:
        return "Player not in summary for some reason"


# more for testing than for use 
def getChipStatus(gameID):
    game = gm.getByID(gameID)
    
    d = {str(player.id): game.bm.chips[player] for player in game.bm.players}
    return d


def getBetStatusAll(gameID, perBettingRound=False):
    game = gm.getByID(gameID)
    # players = gm.getPlayers(gameID)
    dict = game.bm.getBetStatus(perBettingRound)

    return {str(player.id): dict[player] for player in dict.keys()}



# tested 
def getRaiseLimit(gameID, playerID):
    game = gm.getByID(gameID)
    player = pm.getByID(playerID)

    return {playerID: game.bm.getRaiseLimit(player)}

# todo - I want this in terms of max he can bet, not max he can raise
def maxBet(gameID, playerID):
    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    return game.bm.getMaxBet(player)

# tested 
def fold(gameID, playerID):
    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    
    game.bm.fold(player)

    next_bettor = game.bm.nextBettor()

    if next_bettor is not None:
        return {"playerID": str(next_bettor.id)}
    else:
        return "null"


def bet(gameID, playerID, amount, is_raise=False):
    game = gm.getByID(gameID)
    player = pm.getByID(playerID)
    
    game.bm.bet(player, amount, is_raise)
    
    return game.bm.nextBettor()

# note - shouldn't need this!
def getPots(gameID):
    game = gm.getByID(gameID)
    return game.bm.getPots()


# TODO - edit return val
def nextBettor(gameID):
    game = gm.getByID(gameID)
    return game.bm.nextBettor()

    

# TODO - edit return val
def getRaiseStatus(gameID):
    game = gm.getByID(gameID)
    # return game.bm.getRaiseStatus())
    
    d = game.bm.getRaiseStatus()
    temp = {str(player.id): d[player] for player in d.keys()}
    return temp


# TODO - edit return val
def getFoldStatus(gameID):
    game = gm.getByID(gameID)
    dict = game.bm.getFoldStatus()
    dict2 = {str(player.id): dict[player] for player in dict.keys()}

    return dict2




