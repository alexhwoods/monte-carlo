# Author: Alex Woods <alexhwoods@gmail.com>

class Card(object):
    """A card from a standard card deck. Cards have the
    following properties:

    Attributes:
        rank: 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace
        suit: There are four suits - hearts, diamonds, clubs, and spades. They're
              represented as strings.
        faceUp: A boolean, true if the card is faceUp in the game.
    """

    suits = ("CLUBS", "DIAMONDS", "HEARTS", "SPADES")
    # note that 1 is the same as ace
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "JACK", "QUEEN", "KING", "ACE")

    # for sorting out which card is the most valuable in a high card situation
    value = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
             '10':10, 'JACK':11, 'QUEEN':12, 'KING':13, 'ACE':14}

    def __init__(self, suit, rank):
        # making sure suit is entered in the right form
        if suit.upper() in Card.suits:
            self.suit = suit.upper()
        elif not isinstance(suit, basestring):
            raise ValueError("Suit must be a string.")
        else:
            raise ValueError("Invalid suit type, must be of form" + str(Card.suits))

        # making sure rank is entered in the right form
        if rank.upper() in Card.ranks or rank == "1":
            if rank.upper() == "1": rank = "ACE"
            self.rank = rank.upper()
        elif not isinstance(rank, basestring):
            raise ValueError("Rank must be a string")
        else:
            raise ValueError("Must enter a valid rank, of the form " + str(Card.ranks))

        self.faceUp = False

    def same_rank(self, card):
        if self.rank == card.rank:
            return True
        else:
            return False

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def flip(self):
        # I decided it makes no sense to flip a card that's face up back over, in Texas Hold'em at least
        self.faceUp = True

    # DON'T DELETE (it breaks the equality operator)
    def __hash__(self):
        return hash(self.__dict__.values())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        return str(self.rank) + " OF " + str(self.suit)

