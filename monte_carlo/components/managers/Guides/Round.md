# Round - Info about the Round class

Much of the game logic occurs within the Round.py file. A game is 
simply a number of rounds until all players have no more chips left, 
so round is the most important.

I'm implementing as simple a version of Texas Holdem as possible, 
although it would be very easy to make it complete with things such 
as the small and big blind, etc. It's just unnecessary for our purposes.

We'll probably just do 2 players to start out. It will make things 
easier. Going from 2 players to 3 is a big difference, not just in the 
models.

## Attributes:
- *pot* - the number of chips in the center of the table that have been 
put there through betting 
- *community cards* - The 5 cards that sit in the center of the table, 
initially 3 facing up, and 2 facing down. players - these can be 
derived from the game, however, round is not a subclass of game. Within
 a round, each player has 2 hole cards.

## How it works:
A round is one complete hand. Within a round there are 4 betting stages.
The pre-flop, post-flop, post-turn, and the showdown.

Notice the important distinction between rounds and stages. There are 
four stages in a round, and an unlimited number of rounds in a game.


1. ### The Pre-flop ###
All players are dealt **hole cards**. The first betting stage 
("pre-flop") begins. The player left of the dealer *(important 
to keep in mind when doing the GUI)* has to bet first. He can 
    - **call** - meeting the minimum bet (which we'll set, or let 
    the user set) 
    -  **fold** - decide not to play his hand (if all players fold 
    except one, the remaining player gets all the chips in the pot) 
    -  **raise** - bet not only the table minimum, but something extra. 
    All following players in this stage must bet at minimum this new 
    amount. 
    -  **go all-in** - Put all his chips in the pot. This is now the 
    new betting minimum.
    -  If there are two players, player A has 100 chips and player B 
    has 70. If player A wants to go "all-in" we will limit him to 70 
    for simplicity's sake. 
    
2. ### The Flop ### 
Once the pre-flop betting stage is complete, the dealer reveals 
3 cards to the middle of the table. This is called the flop. Another 
stage of betting, the **post-flop** then occurs. The first better 
(the first still active player left of the dealer) has a new option, 
to check.
    - **check** - to pass on the first bet of the stage to the next 
    player. 
    
    If all players in a betting stage check, then the 
    post-flop betting stage is complete. However, if the first 
    player checks and the next player bets, the betting goes all the 
    way around the circle and ends with the original first player, 
    meaning in this case, the original first player would still have to 
    bet.
   
3. ### The Turn ###
Another card is then dealt to the middle of the table. There are now
4 community cards. Another betting stage occurs, called the 
**post-turn**. The post-turn betting stage is identical to the post-flop
betting stage.

4. ### The River ###
The final community card, called the river is dealt to the middle of 
the table. The final betting stage, called the **showdown** occurs. The
players then reveal their cards, and the winner is the one with the hand
with the highest ranking. He gets all the chips in the pot. The round
is now over.


Note - in between rounds, the deck is shuffled.
