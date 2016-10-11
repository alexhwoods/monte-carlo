import sys
# I swear this part was a nightmare to figure out - this has to be accurate!!!!!
sys.path.append("/Users/alexwoods/Desktop/Projects/poker/monte-carlo/")
# print(sys.path)

from monte_carlo.components.models.Game import Game
from monte_carlo.components.models.Round import Round
from monte_carlo.components.models.Player import Player
from monte_carlo import cli
import pprint



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
	6. I'll have to use sysargv or click or some kind of tool in order to allow the
	   user to pass in options about the game.
	7. Go back and build this with click.
'''


''' Assumptions - 
	1. There are 2 players - the user and the AI. (The user's player
	id will be stored in a JSON file, and will be created in initialization.)
	2. Both player will start with 400 chips.
	3. The game has been started (It won't wait for commands).
	4. 
'''
# note - Compile constantly, so you will know if you have any problems!

def chipTester():
	d = cli.getChipStatus(gameID)
	d2 = {}
	d2[user.name] = d[userID]
	d2[aiPlayer.name] = d[aiPlayerID]
	print(str(d2) + "\n")
 
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
print("Game has started!\n")
# # Uncomment to go from round -> game
# while loop condition works!
# while not game.isOver():
# 	print("Entered while loop.")


# Make the mechanics of one round first then put it in while loop
# The first round has been initiated with start game
print(cli.deal(gameID))
print("Dealing...\n")

print("Your cards are: ")
user.hand.show()
print()

# use this to make sure dealing happens correctly!
# print(cli.cardStatus(gameID))

# todo - here you should output the user's card to him

# you're going to have to take user input soon...

chipTester()

cli.startBettingRound(gameID, firstOfRound=True)

while cli.nextBettor(gameID) is not None:
	if cli.nextBettor(gameID) == user:
		print("\n\nUser's options are: " + str(cli.getBettingOptions(gameID, userID)))
		print("Max Bet: " + str(cli.maxBet(gameID, userID)))
		print("Current Bet: " + str(cli.getCurrentBet(gameID)) + "\n")

		# TODO - prompt the user for their move. 
		# remember - MAKE SURE IT'S A VALID MOVE
		# validMoves = ['check', '[number]']
		print("Type 'check' to match the current bet, 'call' to bet 0 if " +
			"nothing has been bet, or an integer X to bet X chips.")

		betMade = False

		while not betMade:
			value = raw_input("Enter betting command: ")
			if value.isdigit():
			    amount = int(value)
			    # if it's a valid amount to bet, bet it.

			    if amount <= cli.maxBet(gameID, userID):
			    	is_raise = False
			    	if amount > cli.getCurrentBet(gameID):
			    		is_raise = True
			    	cli.bet(gameID, userID, amount, is_raise)
			    	betMade = True
			    else:
			    	print("You can only bet " + str(cli.maxBet(gameID, userID)) +
			    		", please enter another betting command.\n")



			else:
				if value.upper() == 'CHECK':
					cli.bet(gameID, userID, cli.getCurrentBet(gameID), is_raise=False)
					betMade = True
				elif value.upper() == 'CALL':
					if cli.getCurrentBet(gameID) == 0:
						cli.bet(gameID, userID, 0, is_raise=False)
						betMade = True
					else:
						print("'call' is not a valid move at this time, since the current " + 
							"bet is non-zero. 'check' will match it.\n")



	else:
		pass
		# THIS IS A DUMMY MOVE
		# TODO - make the AI.
		
		# for now, he'll match the current bet, 
		# or if the user checks, he'll bet min(5, all of his chips)
		currentBet = cli.getCurrentBet(gameID)
		maxBet = cli.maxBet(gameID, aiPlayerID)
		betAmount = 0
		if maxBet >= currentBet:
			betAmount = currentBet
			
		else:
			# TODO - this line isn't good enough because maxBet isn't right
			betAmount = maxBet

		cli.bet(gameID, aiPlayerID, betAmount, is_raise=False)
		print("Anakin bet " + str(betAmount) + ".")


chipTester()











