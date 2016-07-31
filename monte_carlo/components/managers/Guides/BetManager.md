# Guide to BetManager Class
Betting can be a little complicated. I know we're only considering two
player situations for now, but it can still be rough.



 - What happens if Alice has 50 chips and goes all in, but Bob only has
 30 chips? 
    - Bob matches what he can (all 30), and then if Bob wins the round, 
    there is a surplus of 20 that gets returned to Alice.
 
 
## Rules
 - if the betting amount travelling around the table is greater than 
 the amount a player has, he must either go all-in or fold.
 - So in the first round, each player must bet at least the table minimum
 (also called the big blind). 
 - In all following rounds, they have the option to check (or call), to 
 fold, or to raise.
 
 
## Attributes
 - **table minimum** - also called big blind, it's the amount they must
 bet in the first betting round of a dealing round.
 - **players** - the bet manager will need to have access to all the 
 players
 - **short stack** - this is a tuple, (player, amount). This is to handle
 the situation where one player can't match the current betting amount.
 It's because we'll need to return a surplus if that player wins.
 
 
 
### Design Choices
 - Since we are generally designing for 2 players, I'm going to set the
 big blind algorithmically, in order to make it quicker and less 
 cumbersome for the players. It will be set by the formula min(0.5*chips 
 for player with lowest number of chips, 10). If the first number ever 
 lands in a decimal, we will round up (especially important if a player 
 has only 1 chip). 