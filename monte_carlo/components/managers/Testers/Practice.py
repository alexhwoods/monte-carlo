from monte_carlo.components.models.Card import Card
from monte_carlo.components.models.Deck import Deck
from monte_carlo.components.models.Hand import Hand
from monte_carlo.components.models.Player import Player



""" Just became aware of some good python design practices, going to do some refactoring
"""


alex = Player("Alex", 200)
alex.set_hand([Card('spades', '3'), Card('diamonds', '6'), Card('spades', 'king'),
               Card('hearts', '9'), Card('clubs', 'jack')])


comm_cards = [Card('clubs', '2')]

for card in Hand(comm_cards)+alex.hand:
    print(card)
