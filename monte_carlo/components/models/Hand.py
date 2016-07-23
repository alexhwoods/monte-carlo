# Author: Alex Woods <alexhwoods@gmail.com>
from monte_carlo.components.models.Card import Card
from pprint import pprint

class Hand(object):
    """ This is one of the more complicated models. There are still some comparability questions I'm unsure
        about, for example, if we both have two pairs, does it then immediately fall to the high card?

        I'm sure there are some very specific rules out there.

        Note - in Texas Holdem, there are 5 community cards and 2 hole cards per player. This leads to 20 unique
        combinations of 5 cards per player that we'll have to check. That's small enough to just write a for loop,
        so I'll put that logic in the game.

        TODO: I'll finish testing this later, then push it to github.
    """




    hands = ['HIGH_CARD', 'PAIR', 'TWO_PAIRS', 'THREE_OF_A_KIND', 'STRAIGHT', 'FLUSH',
             'FULL_HOUSE', 'FOUR_OF_A_KIND', 'STRAIGHT_FLUSH', 'ROYAL_FLUSH']

    # All of the hands need to be comparable in some way
    value = {'HIGH_CARD': 1, 'PAIR': 2, 'TWO_PAIRS': 3, 'THREE_OF_A_KIND': 4, 'STRAIGHT': 5, 'FLUSH': 6,
             'FULL_HOUSE': 7, 'FOUR_OF_A_KIND': 8, 'STRAIGHT_FLUSH': 9, 'ROYAL_FLUSH': 10}

    def __init__(self, arr):
        # the next 4 lines are so the hand is sorted in order by rank
        card_rank = []
        for i in arr:
            card_rank.append((i, Card.value[i.get_rank()]))

        temp = sorted(card_rank, key=lambda x: x[1])
        self.cards = [x[0] for x in temp]

        # the ranks,suits of all the cards in the hand. Useful for calculating what a hand is
        self.ranks = [card.get_rank() for card in self.cards]
        self.suits = [card.get_suit() for card in self.cards]

    def type(self):
        """ There's a bit of inclusivity, which is why I'm going from the top down than the bottom up.

                For example, a royal flush is always a flush, but a flush is not always a royal flush.
             So it's necessary to check royal flush before you check flush, otherwise I would have to write
             something like 'elif self.flush() and not royal_flush(): ...', and that's more cumbersome.
        """

        if self.straight_flush():
            return 'STRAIGHT_FLUSH'
        elif self.straight_flush():
            return 'STRAIGHT_FLUSH'
        elif self.four_of_a_kind():
            return 'FOUR_OF_A_KIND'
        elif self.full_house():
            return 'FULL_HOUSE'
        elif self.flush():
            return 'FLUSH'
        elif self.straight():
            return 'STRAIGHT'
        elif self.three_of_a_kind():
            return 'THREE_OF_A_KIND'
        elif self.num_pairs() == 2:
            return 'TWO_PAIRS'
        elif self.num_pairs() == 1:
            return 'PAIR'
        else:
            return 'HIGH_CARD'


    def high_card(self):
        return self.ranks[-1]

    # pairs are done a little differently than three or four of a kind, since there can be 1 or 2 of them
    def get_pairs(self):
        pairs = [f for f in set(self.ranks) if self.ranks.count(f) == 2]
        return pairs

    def num_pairs(self):
        return len(self.get_pairs())

    def three_of_a_kind(self):
        return len([f for f in set(self.ranks) if self.ranks.count(f) == 3]) == 1

    # this is very pigeonhole-ish
    def straight(self):
        # every straight contains either a 5 or a 10
        if '5' not in self.ranks and '10' not in self.ranks:
            return False

        # the lowest and highest card in the hand must be 4 apart in value
        if Card.value[self.ranks[-1]] - Card.value[self.ranks[0]] != 4:
            return False

        # catches any repeated ranks
        if len(set(self.ranks)) < 5:
            print(len(set(self.ranks)))
            return False

        return True

    def flush(self):
        return len(set(self.suits)) <= 1

    def full_house(self):
        return self.num_pairs() == 1 and self.three_of_a_kind()

    # the more valuable hands are so easy :)
    def straight_flush(self):
        return self.straight() and self.flush()

    def four_of_a_kind(self):
        return len([f for f in set(self.ranks) if self.ranks.count(f) == 3]) == 1

    def royal_flush(self):
        return self.straight_flush() and self.high_card() == 'ACE'

    def show(self):
        arr = []
        for i in self.cards:
            arr.append(str(i))
        pprint(arr)
        print("\n")




# currently there is a straight in this hand
# hand1 = Hand([Card('spades', 'ACE'), Card('DIAMONDS', 'KING'), Card('DIAMONDS', 'QUEEN'),
#               Card('DIAMONDS', 'JACK'), Card('DIAMONDS', '9')])
#
# hand1.show()
# print(hand1.type())