# TODO Things to test. Errors I got, etc

""""" Note that these are the ones where it failed. For each failure, there were 6 successes at least.
      The fact is hands such as a flush or a straight are just really improbable, but we definitely need
      to test the edge cases.
"""""

"""""  Test Case # 1
table cards:
['KING OF HEARTS',
 'ACE OF CLUBS',
 'KING OF SPADES',
 '3 OF CLUBS',
 '2 OF HEARTS']

Bob - ['8 OF HEARTS', 'QUEEN OF HEARTS']
Carla - ['4 OF CLUBS', 'JACK OF SPADES']
and they tied, when Bob should have won.
"""""

""""" Test Case #2

The table cards are:
['KING OF HEARTS',
 '3 OF HEARTS',
 '6 OF CLUBS',
 'QUEEN OF DIAMONDS',
 '7 OF HEARTS']

 Carla - ['JACK OF SPADES', 'ACE OF DIAMONDS']
 Bob - ['3 OF DIAMONDS', 'ACE OF CLUBS']
 Carlos - ['2 OF SPADES', '6 OF DIAMONDS']

 Carlos should have won, with a pair of 6's (higher than Bob's pair of 3's). However Bob and Carla were pronounced the winners. I think it's because
 Carlos's pair and Bob's pair cancelled each other out, and then Bob and Carla tied on a high card.
"""""

""""" Test Case #3
The table cards are:
['5 OF HEARTS',
 '3 OF DIAMONDS',
 'KING OF SPADES',
 '6 OF HEARTS',
 'KING OF HEARTS']

 Carla - ['6 OF DIAMONDS', '10 OF DIAMONDS']
 Bob - ['3 OF HEARTS', '4 OF CLUBS']
 Carlos - ['6 OF CLUBS', '7 OF SPADES']

 It says at first that they all have a straight; none of them should. (Test straight() function in Hand.py).
 Then it says they all have two pairs, which is correct, then one pair, still correct.

 Then awards them all the win because of the high card. I see the problem here - only check the two hole cards for high
 card.

 And probably also the straight() function is broken.

"""""

""""" Test Case #4

{'Bob, 330': 1, 'Carla, 180': 2, 'Carlos, 280': 2}
The winners pre-highcard are:
Carlos
Carla
{'Bob, 330': 1, 'Carla, 180': 1, 'Carlos, 280': 1}
The winners pre-highcard are:
Carlos
Bob
Carla
The winner of the round is ['Carlos, 280']
Their hands were:
['HIGH_CARD']
They won 60

Look at the above. Bob is clearly out of it, but he manages to sneak back into consideration! It's not
weeding him out effectively when he doesn't have the max score.


"""""

# TODO - one that gives a clear issue. Pairs can be decided among themselves.
""""" Test Case #5

The case where Player A has a pair of queens, Player B a pair of fours, and Player B has an ace.
The algorithm would give the win to player B, but I think with pairs a higher pair wins.


"""""

""""" Test Case #5

 The table cards are:
['9 OF SPADES', '7 OF CLUBS', '3 OF HEARTS', '5 OF DIAMONDS', '6 OF DIAMONDS']

Silvia - ['3 OF SPADES', '3 OF CLUBS']
Randolf - ['10 OF HEARTS', '10 OF DIAMONDS']

It said Sylvia has a four of a kind?

"""""

# TODO - easy fix, just turning an if statement to a while loop
""""" Test Case #6

If two players tie on a high card, it doesn't go to the next card down.

"""""

""""" Test Case #7


"""""

""""" Test Case #8


"""""

""""" Test Case #2


"""""