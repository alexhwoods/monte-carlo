import sys
# I swear this part was a nightmare to figure out
sys.path.append("/Users/alexwoods/Desktop/Projects/poker/monte-carlo/")

from monte_carlo.components.models.Game import Game
from monte_carlo.components.models.Round import Round
from monte_carlo.components.models.Player import Player
from monte_carlo import cli



''' Things Learned While Writing This
	1. The user's name should be the super user on the operating system.
	2. I'm going to have to figure out how to manage these players. 
	   Since they're are only two, it might be worth not having a player manager
	   for this version of the project
	3. Going through the CLI is better for the more complicated methods. For the 
	   simple ones, it's just cumbersome. (betting and dealing go through CLI)
	   As a general rule, don't touch the betting manager.
	4. Remember - bad requests break things!!!
	5. Give the user the option to have things explained to him as the game moves
	   along (i.e. what does 'check' mean)
'''


''' Assumptions - 
	1. There are 2 players - the user and the AI. (The user's player
	id will be stored in a JSON file, and will be created in initialization.)
	2. Both player will start with 400 chips.
	3. The game has been started (It won't wait for commands).
	4. 
'''
# note - Compile constantly, so you will know if you have any problems!

 
# Setting Things Up

startingChips = 400
user = cli.createPlayer("User", startingChips)
userID = str(user.id)

aiPlayer = cli.createPlayer("Anakin", startingChips)
aiPlayerID = str(aiPlayer.id)

game = cli.createGame()
gameID = str(game.id)     # for when I need to go through the CLI

game.add_player(user)
game.add_player(aiPlayer)


# starts the game!
game.start()

# # Uncomment to go from round -> game
# while loop condition works!
# while not game.isOver():
# 	print("Entered while loop.")


# Make the mechanics of one round first then put it in while loop
# The first round has been initiated with start game
print(cli.deal(gameID))


# use this to make sure dealing happens correctly!
print(cli.cardStatus(gameID))

# todo - here you should output the user's card to him

# you're going to have to take user input soon...

cli.startBettingRound(gameID, firstOfRound=True)

while cli.nextBettor(gameID) is not None:
	if cli.nextBettor(gameID) == user:
		print("\n\nUser's options are: " + str(cli.getBettingOptions(gameID, userID)))
		print("Max Bet: " + str(cli.maxBet(gameID, userID)))
		print("Current Bet: " + str(cli.getCurrentBet(gameID)))

		# TODO - prompt the user for their move. 
		# remember - MAKE SURE IT'S A VALID MOVE
	else:
		pass
		# it's the Anakin's turn to bet
		# in the future the AI's move will go here, for now it will
		# be a dummy move.
		# The dummy move will never be folding, but the real AI might 
		# make that move
		
		# for now, he'll match the current bet, 
		# or if the user checks, he'll bet min(5, all of his chips)
		currentBet = cli.getCurrentBet(gameID)
		maxBet = cli.maxBet(gameID, aiPlayerID)
		if maxBet >= currentBet:
			cli.bet(gameID, aiPlayerID, currentBet, is_raise=False)
		else:
			# TODO - this line isn't good enough because maxBet isn't right
			cli.bet(gameID, aiPlayerID, maxBet, is_raise=False)
	

	break











