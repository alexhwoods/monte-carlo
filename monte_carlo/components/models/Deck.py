# Author: Alex Woods <alexhwoods@gmail.com>

from monte_carlo.components.models.Card import Card
from itertools import product
from pprint import pprint
import collections
import random


class Deck(object):
    """A standard deck of playing cards, minus the jokers. A deck will have the
    following properties:

    Attributes:
        cards: an stack of cards. It is a stack, not just a plain array. Initially sorted, clubs, diamonds, hearts,
               spades, with the rank sub-sorted among each suit.

        The right end of the deck will be the top, and the left end will be the bottom. I'm making this choice
        because of the nature of the pop() function.

        draw(): equivalent to pop(), but in poker terminology. Returns a card from the top of the deck, and removes
                it from the deck as well.

        pushBottom(): Takes a handful of cards (1 or many), and appends them to the bottom of the deck, as would
                      happen in a casino.

        show(): prints the deck in a nice human readable form



    """

    def __init__(self):
        self._cards = collections.deque()
        for i,j in product(Card.suits, Card.ranks):
            self._cards.append(Card(i, j))

    def draw_one(self):
        return self._cards.pop()

    # to draw multiple cards
    def draw_many(self, num__cards=1):
        arr = []
        for i in range(num__cards):
            arr.append(self._cards.pop())

        return arr

    # can handle the case where you push 1 card to the bottom, or multiple.
    # TODO make this function more robust, so that the deck is a closed system
    def push_bottom(self, card):
        if isinstance(card, Card):
            card = [card]

        for i in range(len(card)):
            self._cards.appendleft(card[i])

    def shuffle(self):
        random.shuffle(self._cards)

    def is_full(self):
        return set(self._cards) == set([Card(i,j) for i, j in product(Card.suits, Card.ranks)])
    
    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)

    def show(self):
        arr = []
        for i in self._cards:
            arr.append(str(i))
        print("Starting at the bottom of the deck...")
        pprint(arr)

