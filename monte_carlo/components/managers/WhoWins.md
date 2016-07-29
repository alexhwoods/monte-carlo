# Rules of Comparability
1. You must make the best hand possible using exactly 5 cards.
2. All five cards are used in deciding the strength of the hand.
3. Once the strongest 5 cards are chosen, no cards outside it have any
   bearing on the strength of the hand.

### Common Areas of Confusion
- Two players have a flush - The player with the highest flush wins. That
is, pick out the 5 cards that give the flush (for both players), and
 then the highest card between those two hands will be the winner.
    - Note - the way our algorithm currently is, it doesn't do this. I'll
    make an attribute in player called "best round hand", and then attach
    the best hand of the round on that, so for ties we can calculate things
    more easily.
- Two players have two pairs. Again, we can solve this by sorting out the
5 cards that represent the players chosen best hand. Then, the highest pair
wins. Say player 1 has a pair of aces and a pair of 3's, player 2 has a 
pair of king's and a pair of queen's. Player 1 wins.



### Thoughts
After reading more about this, I think I'll need to write an function in
hand to pull out the hand of the highest worth, then I'll compare only
those two hands in the get winner function (assuming we have 2 players). 

