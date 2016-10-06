# Author: Alex Woods <alexhwoods@gmail.com>
from components.models.Card import Card
from itertools import combinations
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
        self.cards.reverse()

        # the ranks,suits of all the cards in the hand. Useful for calculating what a hand is
        self.ranks = [card.get_rank() for card in self.cards]
        self.suits = [card.get_suit() for card in self.cards]

    @staticmethod
    def get_best_hand(cards):
        """ Given an array of 7 cards (because texas holdem is played with 2 hole cards and 5 community cards),
            players must choose the best 5 cards combo they can, and then are judged only on that.

            I'll first write a function that compares two hands and proclaims a winner. I'll then use that
            to get the individuals best hand. (The rest of the logic will be in round.py)

            (tested and works!)
        """
        hands = []
        for combo in list(combinations(cards, 5)):
            temp = Hand(combo)
            hands.append(temp)

        best_hand = hands[0]
        for hand in hands:
            if Hand.winner(best_hand, hand) == hand:
                best_hand = hand

        return best_hand

    @staticmethod
    def winner(hand1, hand2):
        """ A function to compare two hands and pronounce a winner. Once this is written, the models are
        half done.

        If this function returns None, it is a tie, and the players split the pot.

        (Tested and works!)

        :param hand1: Hand object
        :param hand2: Hand object
        :return: either hand1, hand2, or None
        """

        # 'ROYAL_FLUSH'
        # impossible for both to have at once
        if hand1.type() == 'ROYAL_FLUSH': return hand1
        elif hand2.type() == 'ROYAL_FLUSH': return hand2

        # 'STRAIGHT_FLUSH'
        if hand1.type() == 'STRAIGHT_FLUSH' and hand2.type() != 'STRAIGHT_FLUSH': return hand1
        elif hand2.type() == 'STRAIGHT_FLUSH' and hand1.type() != 'STRAIGHT_FLUSH': return hand2
        elif hand1.type() == 'STRAIGHT_FLUSH' and hand2.type() == 'STRAIGHT_FLUSH':
            return Hand.has_highest_card(hand1, hand2)

        # 'FOUR_OF_A_KIND'
        # if only one has four of a kind, it wins. If both have it, then
        # the player with the higher set of 4 wins, and if it's the same set of 4, then
        # the player with the highest card (the kicker) wins.
        if hand1.type() == 'FOUR_OF_A_KIND' and hand2.type() != 'FOUR_OF_A_KIND': return hand1
        elif hand2.type() == 'FOUR_OF_A_KIND' and hand1.type() != 'FOUR_OF_A_KIND': return hand2
        elif hand1.type() == 'FOUR_OF_A_KIND' and hand2.type() == 'FOUR_OF_A_KIND':
            if Card.value[hand1.get_four_of_a_kind()] > Card.value[hand2.get_four_of_a_kind()]:
                return hand1
            elif Card.value[hand2.get_four_of_a_kind()] > Card.value[hand1.get_four_of_a_kind()]:
                return hand2
            else:
                return Hand.has_highest_card(hand1, hand2)

        # 'FULL_HOUSE'
        if hand1.type() == 'FULL_HOUSE' and hand2.type() != 'FULL_HOUSE':
            return hand1
        elif hand2.type() == 'FULL_HOUSE' and hand1.type() != 'FULL_HOUSE':
            return hand2
        elif hand1.type() == 'FULL_HOUSE' and hand2.type() == 'FULL_HOUSE':
            if Card.value[hand1.get_three_of_a_kind()] > Card.value[hand2.get_three_of_a_kind()]:
                return hand1
            elif Card.value[hand2.get_three_of_a_kind()] > Card.value[hand1.get_three_of_a_kind()]:
                return hand2
            else:
                # now I have to check the pairs and see which is higher!
                if Card.value[hand1.get_pairs()[0]] > Card.value[hand2.get_pairs()[0]]:
                    return hand1
                elif Card.value[hand2.get_pairs()[0]] > Card.value[hand1.get_pairs()[0]]:
                    return hand2
                else:
                    return None

        # 'FLUSH'
        if hand1.type() == 'FLUSH' and hand2.type() != 'FLUSH':
            return hand1
        elif hand2.type() == 'FLUSH' and hand1.type() != 'FLUSH':
            return hand2
        elif hand1.type() == 'FLUSH' and hand2.type() == 'FLUSH':
            return Hand.has_highest_card(hand1, hand2)


        # 'STRAIGHT'
        if hand1.type() == 'STRAIGHT' and hand2.type() != 'STRAIGHT':
            return hand1
        elif hand2.type() == 'STRAIGHT' and hand1.type() != 'STRAIGHT':
            return hand2
        elif hand1.type() == 'STRAIGHT' and hand2.type() == 'STRAIGHT':
            return Hand.has_highest_card(hand1, hand2)

        
        # 'THREE_OF_A_KIND'
        if hand1.type() == 'THREE_OF_A_KIND' and hand2.type() != 'THREE_OF_A_KIND':
            return hand1
        elif hand2.type() == 'THREE_OF_A_KIND' and hand1.type() != 'THREE_OF_A_KIND':
            return hand2
        elif hand1.type() == 'THREE_OF_A_KIND' and hand2.type() == 'THREE_OF_A_KIND':
            if Card.value[hand1.get_three_of_a_kind()] > Card.value[hand2.get_three_of_a_kind()]:
                return hand1
            elif Card.value[hand2.get_three_of_a_kind()] > Card.value[hand1.get_three_of_a_kind()]:
                return hand2
            else:
                return Hand.has_highest_card(hand1, hand2)

        # 'TWO_PAIRS'
        if hand1.num_pairs() == 2 and hand2.num_pairs() != 2: return hand1
        if hand2.num_pairs() == 2 and hand1.num_pairs() != 2: return hand2
        elif hand1.num_pairs() == 2 and hand2.num_pairs() == 2:
            vals1, vals2 = [Card.value[x] for x in hand1.get_pairs()], [Card.value[x] for x in hand2.get_pairs()]
            vals1, vals2 = sorted(vals1), sorted(vals2)

            vals1.reverse()
            vals2.reverse()

            for i in range(2):
                if vals1[i] > vals2[i]:
                    return hand1
                elif vals2[i] > vals1[i]:
                    return hand2

            return Hand.has_highest_card(hand1, hand2)

        # 'PAIR'
        if hand1.type() == 'PAIR' and hand2.type() != 'PAIR':
            return hand1
        elif hand2.type() == 'PAIR' and hand1.type() != 'PAIR':
            return hand2
        elif hand1.type() == 'PAIR' and hand2.type() == 'PAIR':
            if Card.value[hand1.get_pairs()[0]] > Card.value[hand2.get_pairs()[0]]:
                return hand1
            elif Card.value[hand2.get_pairs()[0]] > Card.value[hand1.get_pairs()[0]]:
                return hand2
            else:
                return Hand.has_highest_card(hand1, hand2)

        # 'HIGH_CARD'
        return Hand.has_highest_card(hand1, hand2)


    # tested and works
    @staticmethod
    def has_highest_card(hand1, hand2):
        for i in range(5):
            if Card.value[hand1.cards[i].get_rank()] > Card.value[hand2.cards[i].get_rank()]: return hand1
            elif Card.value[hand2.cards[i].get_rank()] > Card.value[hand1.cards[i].get_rank()]: return hand2
            else: pass

        return None


    def type(self, disabled_hands=[]):
        """ There's a bit of inclusivity, which is why I'm going from the top down than the bottom up.

                For example, a royal flush is always a flush, but a flush is not always a royal flush.
             So it's necessary to check royal flush before you check flush, otherwise I would have to write
             something like 'elif self.flush() and not royal_flush(): ...', and that's more cumbersome.
        """

        if self.royal_flush() and 'ROYAL_FLUSH' not in disabled_hands:
            return 'ROYAL_FLUSH'
        elif self.straight_flush() and 'STRAIGHT_FLUSH' not in disabled_hands:
            return 'STRAIGHT_FLUSH'
        elif self.four_of_a_kind() and 'FOUR_OF_A_KIND' not in disabled_hands:
            return 'FOUR_OF_A_KIND'
        elif self.full_house() and 'FULL_HOUSE' not in disabled_hands:
            return 'FULL_HOUSE'
        elif self.flush() and 'FLUSH' not in disabled_hands:
            return 'FLUSH'
        elif self.straight() and 'STRAIGHT' not in disabled_hands:
            return 'STRAIGHT'
        elif self.three_of_a_kind() and 'THREE_OF_A_KIND' not in disabled_hands:
            return 'THREE_OF_A_KIND'
        elif self.num_pairs() == 2 and 'TWO_PAIRS' not in disabled_hands:
            return 'TWO_PAIRS'
        elif self.num_pairs() == 1 and 'PAIR' not in disabled_hands:
            return 'PAIR'
        else:
            return 'HIGH_CARD'


    def high_card(self):
        return self.ranks[0]

    # pairs are done a little differently than three or four of a kind, since there can be 1 or 2 of them
    # doesn't return a sorted list! The values are strings not int in the list
    def get_pairs(self):
        pairs = [f for f in set(self.ranks) if self.ranks.count(f) == 2]
        return pairs

    def num_pairs(self):
        return len(self.get_pairs())

    def three_of_a_kind(self):
        return len([f for f in set(self.ranks) if self.ranks.count(f) == 3]) == 1

    def get_three_of_a_kind(self):
        if self.three_of_a_kind():
            num = list(set([f for f in set(self.ranks) if self.ranks.count(f) == 3]))
            return num[0]
        else:
            return None

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
        return len([f for f in set(self.ranks) if self.ranks.count(f) == 4]) == 1

    def get_four_of_a_kind(self):
        if self.four_of_a_kind():
            num = list(set([f for f in set(self.ranks) if self.ranks.count(f) == 4]))
            return num[0]
        else:
            return None

    def royal_flush(self):
        return self.straight_flush() and self.high_card() == 'ACE'

    def __getitem__(self, position):
        return self.cards[position]

    def __add__(self, other):
        cards = self.cards + other.cards
        return cards

    def show(self, ascending=False):
        arr = []
        for i in self.cards:
            arr.append(str(i))
        if ascending:
            arr.reverse()
        pprint(arr)
