# Betting

I have just a basic idea on how this works, and it can get confusing.
My current implementation sucks, and is full of holes. Rather than plug
the holes, I'd like to make a simple, robust system.

I'll consider this in the context of a game between Bob and Alice. Note
that we are playing No-Limit Texas Hold'em.

I think I'll need a BetManager class, too much logic has been put in 
Round.

### Questions
 - What happens if Alice has 400 chips, Bob has 10, and Bob bets all in
 on the first betting round? What are Alice's options for betting?
 - adf
 
 
 
 
 
## Some Definitions
  - **call** - to match the previous bet
  - **check** - to check is the same as to call, except there is no 
  previous bet
  - **fold** - to throw away your hand and wait until the next deal to
  play again
  - **raise** - to bet more than the previous bet