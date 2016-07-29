from monte_carlo.components.models.Hand import Hand
from monte_carlo.components.models.Card import Card

""" Testing two hands squaring off, and a get_best_hand function


"""

' **************************** Testing Best Hand *********************** '
""" TEST CASE 1 (best hand)
(input)
community cards = ['KING', '9', '9', '9', '9']
player A = ['ACE', '2']
player B = ['KING', 'KING']

(output)
player A = ['9', '9', '9', '9', 'ACE']
player B = ['9', '9', '9', '9', 'KING']


Player A wins, because the four of a kind's cancel and the ace is a stronger high card than the king.

"""
# code goes here






""" TEST CASE 2

(input)
community cards = ['KING', 'QUEEN', '2', '3', '2']
player A = ['ACE', 'ACE']
player B = ['KING', 'QUEEN']

(output)
player A = ['ACE', 'ACE', '2', '2', 'KING']
player B = ['KING', 'KING', 'QUEEN', 'QUEEN', '3']

Player A wins, because in a two-pair situation the tie-breaker is the rank of the first pair.

"""
# code goes here






""" TEST CASE 3

"""

# code goes here



print(" \n Now Testing Hand.winner() function. \n ")

' ************************** Testing Winning Hand ************************* '

# Royal Flush
""" TEST CASE 1 - royal flush with winner
hand1 = ['10 of diamonds', 'jack of diamonds', 'queen of diamonds', 'king of diamonds', 'ace of diamonds']
hand2 = ['8', '8', '8', 'QUEEN', 'QUEEN']

hand1, it has a royal flush.

"""
hand1 = Hand([Card('diamonds', '10'), Card('diamonds', 'jack'), Card('diamonds', 'queen'),
              Card('diamonds', 'king'), Card('diamonds', 'ace')])
hand2 = Hand([Card('spades', '8'), Card('hearts', '8'), Card('diamonds', 'ace'),
              Card('diamonds', 'king'), Card('diamonds', '10')])


if Hand.winner(hand1, hand2) == hand1:
    print("TEST CASE 1: CORRECT")
else:
    print("ERROR IN TEST CASE 1")





# straight flush
""" TEST CASE 2 
hand1 = ['5 of spades', '6 of spades', '7 of spades', '8 of spades', '9 of spades']
hand2 = ['8 of hearts', '9 of hearts', '10 of hearts', 'JACK of hearts', 'QUEEN of hearts']

hand2, it has the higher straight flush.

"""
hand1 = Hand([Card('spades', '5'), Card('spades', '6'), Card('spades', '7'),
              Card('spades', '8'), Card('spades', '9')])
hand2 = Hand([Card('hearts', '8'), Card('hearts', '9'), Card('hearts', '10'),
              Card('hearts', 'jack'), Card('hearts', 'queen')])

if Hand.winner(hand1, hand2) == hand2:
    print("TEST CASE 2: CORRECT")
else:
    print("ERROR IN TEST CASE 2")


# Four of a kind
""" TEST CASE 3 - four of a kind with winner by 4-set
Two TODO: hand type heres
hand1 = ['5', '5', '5', '5', 'ACE']
hand2 = ['8', '8', '8', '8', '2']

hand2

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', '5'), Card('spades', 'ace')])
hand2 = Hand([Card('spades', '8'), Card('hearts', '8'), Card('diamonds', '8'),
              Card('clubs', '8'), Card('spades', '2')])

if Hand.winner(hand1, hand2) == hand2:
    print("TEST CASE 3: CORRECT")
else:
    print("ERROR IN TEST CASE 3")




""" TEST CASE 3.5 - four of a kind with winner by high card
Two TODO: hand type heres
hand1 = ['5', '5', '5', '5', 'ACE']
hand2 = ['5', '5', '5', '5', 'queen']

hand1

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', '5'), Card('spades', 'ace')])
hand2 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', '5'), Card('spades', 'queen')])

if Hand.winner(hand1, hand2) == hand1:
    print("TEST CASE 3.5: CORRECT")
else:
    print("ERROR IN TEST CASE 3.5")


# Full House
""" TEST CASE 4 - three of a kind decide (normal)
Two full houses
hand1 = ['5', '5', '5', 'ACE', 'ACE']
hand2 = ['8', '8', '8', 'QUEEN', 'QUEEN']

hand2 should win, because the set of three is the more important one here. If the sets of three are equal, 
then it goes to the sets of two.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', 'ace'), Card('spades', 'ace')])
hand2 = Hand([Card('spades', '8'), Card('hearts', '8'), Card('diamonds', '8'),
              Card('clubs', 'queen'), Card('spades', 'queen')])

if Hand.winner(hand1, hand2) == hand2:
    print("TEST CASE 4: CORRECT")
else:
    print("ERROR IN TEST CASE 4")



""" TEST CASE 5 - Full house pair decide
Two full houses
hand1 = ['5', '5', '5', 'ACE', 'ACE']
hand2 = ['5', '5', '5', 'QUEEN', 'QUEEN']

hand1 should win.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', 'ace'), Card('spades', 'ace')])
hand2 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', 'queen'), Card('spades', 'queen')])

if Hand.winner(hand1, hand2) == hand1:
    print("TEST CASE 5: CORRECT")
else:
    print("ERROR IN TEST CASE 5")



""" TEST CASE 6 - Full house tie
Two full houses
hand1 = ['5', '5', '5', 'ACE', 'ACE']
hand2 = ['5', '5', '5', 'ACE', 'ACE']

A tie. Keep in mind this is possible in Texas Holdem due to community cards.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', 'ace'), Card('spades', 'ace')])
hand2 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', 'ace'), Card('spades', 'ace')])

if Hand.winner(hand1, hand2) is None:
    print("TEST CASE 6: CORRECT")
else:
    print("ERROR IN TEST CASE 6")


# straight
""" TEST CASE 7 - Straight with a winner

hand1 = ['5', '6', '7', '8', '9']
hand2 = ['8', '9', '10', 'JACK', 'QUEEN']

hand2 wins. They both have a straight, but hand2 has the higher card.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '6'), Card('spades', '7'),
              Card('diamonds', '8'), Card('spades', '9')])
hand2 = Hand([Card('diamonds', '8'), Card('spades', '9'), Card('hearts', '10'),
              Card('spades', 'jack'), Card('hearts', 'queen')])

if Hand.winner(hand1, hand2) == hand2:
    print("TEST CASE 7: CORRECT")
else:
    print("ERROR IN TEST CASE 7")



""" TEST CASE 8 - Straight without a winner

hand1 = ['5', '6', '7', '8', '9']
hand2 = ['5', '6', '7', '8', '9']

Tie.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '6'), Card('spades', '7'),
              Card('diamonds', '8'), Card('spades', '9')])
hand2 = Hand([Card('spades', '5'), Card('hearts', '6'), Card('spades', '7'),
              Card('diamonds', '8'), Card('spades', '9')])

if Hand.winner(hand1, hand2) is None:
    print("TEST CASE 8: CORRECT")
else:
    print("ERROR IN TEST CASE 8")


# flush
""" TEST CASE 9 - Flush with a winner

hand1 = ['5 of spades', '6 of spades', '2 of spades', '8 of spades', 'queen of spades']
hand2 = ['2 of clubs', '6 of clubs', '10 of clubs', 'JACK of clubs', 'ace of clubs']

hand2 wins. They both have a flush, but hand2 has the higher card, an ace.

"""
hand1 = Hand([Card('spades', '5'), Card('spades', '6'), Card('spades', '2'),
              Card('spades', '8'), Card('spades', 'queen')])
hand2 = Hand([Card('clubs', '2'), Card('clubs', '6'), Card('clubs', '10'),
              Card('clubs', 'jack'), Card('clubs', 'ace')])

if Hand.winner(hand1, hand2) == hand2:
    print("TEST CASE 9: CORRECT")
else:
    print("ERROR IN TEST CASE 9")


""" TEST CASE 10 - Flush with a tie

hand1 = ['5 of spades', '6 of spades', '2 of spades', '8 of spades', 'queen of spades']
hand2 = ['5 of clubs', '6 of clubs', '2 of clubs', '8 of clubs', 'queen of clubs']

Tie. They both have a flush but neither has a higher unique card

"""
# impossible situation, but whatever
hand1 = Hand([Card('spades', '5'), Card('spades', '6'), Card('spades', '2'),
              Card('spades', '8'), Card('spades', 'queen')])
hand2 = Hand([Card('clubs', '5'), Card('clubs', '6'), Card('clubs', '2'),
              Card('clubs', '8'), Card('clubs', 'queen')])

if Hand.winner(hand1, hand2) is None and Hand.winner(hand1, hand1) is None:
    print("TEST CASE 10: CORRECT")
else:
    print("ERROR IN TEST CASE 10")



# Three of a kind
""" TEST CASE 11 - three of a kind with winner

hand1 = ['5', '5', '5', '8', 'queen']
hand2 = ['10', '10', '10', '8', 'queen']

hand2. His 3-set is higher.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', '8'), Card('spades', 'queen')])
hand2 = Hand([Card('spades', '10'), Card('hearts', '10'), Card('diamonds', '10'),
              Card('clubs', '8'), Card('spades', 'queen')])

if Hand.winner(hand1, hand2) == hand2:
    print("TEST CASE 11: CORRECT")
else:
    print("ERROR IN TEST CASE 11")



""" TEST CASE 12 - three of a kind with winner by high card

hand1 = ['5', '5', '5', '8', 'queen']
hand2 = ['5', '5', '5', '8', '10']

hand1. The 3-sets tie but his high-card is better.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', '8'), Card('spades', 'queen')])
hand2 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '5'),
              Card('clubs', '8'), Card('spades', '10')])

if Hand.winner(hand1, hand2) == hand1:
    print("TEST CASE 12: CORRECT")
else:
    print("ERROR IN TEST CASE 12")



# Two pairs

# TODO There is an error when they both have two unqeual pairs
""" TEST CASE 13 - two pairs with a winner by first pair

hand1 = ['5', '5', '10', '10', 'queen']
hand2 = ['5', '5', '2', '2', '10']

hand1. It's first pair (10's) is higher than hand2's first pair of 5's.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '10'),
              Card('clubs', '10'), Card('spades', 'queen')])
hand2 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '2'),
              Card('clubs', '2'), Card('spades', '10')])

if Hand.winner(hand1, hand2) == hand1:
    print("TEST CASE 13: CORRECT")
else:
    print("ERROR IN TEST CASE 13")




""" TEST CASE 14 - two pairs with a winner by second pair

hand1 = ['5', '5', '3', '3', '2']
hand2 = ['5', '5', '2', '2', '10']

hand1. It's second pair (3's) is higher than hand2's first pair of 2's.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '3'),
              Card('clubs', '3'), Card('spades', '2')])
hand2 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '2'),
              Card('clubs', '2'), Card('spades', '10')])

if Hand.winner(hand1, hand2) == hand1:
    print("TEST CASE 14: CORRECT")
else:
    print("ERROR IN TEST CASE 14")



""" TEST CASE 15 - two pairs with a winner by high card

hand1 = ['5', '5', '3', '3', '2']
hand2 = ['5', '5', '3', '3', '10']

hand2. The two hands have the same pairs, but hand2 has a better kicker.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '3'),
              Card('clubs', '3'), Card('spades', '2')])
hand2 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '3'),
              Card('clubs', '3'), Card('spades', '10')])

if Hand.winner(hand1, hand2) == hand2:
    print("TEST CASE 15: CORRECT")
else:
    print("ERROR IN TEST CASE 15")



# pair
""" TEST CASE 16 - two unequal pairs

hand1 = ['5', '5', '3', 'ace', 'jack']
hand2 = ['queen', 'queen', '3', 'king', '10']

hand2. It's pair is higher.

"""
hand1 = Hand([Card('spades', '5'), Card('hearts', '5'), Card('diamonds', '3'),
              Card('clubs', 'ace'), Card('spades', 'jack')])
hand2 = Hand([Card('spades', 'queen'), Card('hearts', 'queen'), Card('diamonds', '3'),
              Card('clubs', 'king'), Card('spades', '10')])

if Hand.winner(hand1, hand2) == hand2:
    print("TEST CASE 16: CORRECT")
else:
    print("ERROR IN TEST CASE 16")


""" TEST CASE 17 - two equal pairs

hand1 = ['queen', 'queen', '4', 'ace', 'jack']
hand2 = ['queen', 'queen', '3', 'king', '10']

hand1. Win by high card

"""
hand1 = Hand([Card('spades', 'queen'), Card('hearts', 'queen'), Card('diamonds', '4'),
              Card('clubs', 'ace'), Card('spades', 'jack')])
hand2 = Hand([Card('spades', 'queen'), Card('hearts', 'queen'), Card('diamonds', '3'),
              Card('clubs', 'king'), Card('spades', '10')])

if Hand.winner(hand1, hand2) == hand1:
    print("TEST CASE 17: CORRECT")
else:
    print("ERROR IN TEST CASE 17")











""" ************************************** Just testing other stuff **********************************
"""










