from monte_carlo.components.models.Player import Player
from monte_carlo.components.models.Hand import Hand
from monte_carlo.components.models.Pot import Pot
from collections import namedtuple
import math
from pprint import pprint

# these things rock, it's like a baby object
Surplus = namedtuple('Surplus', ['player', 'amount'])
Bet = namedtuple('Bet', ['player', 'amount'])


class BetManager(object):

    betting_options = ['CALL', 'CHECK', 'RAISE', 'FOLD']

    def __init__(self, round):
        self.round = round
        self.players = round.players
        self.chips = {player: player.chips for player in self.players}
        self.chips_at_beginning = {player: player.chips for player in self.players}

        # there is initially one pot, namely, the main pot.
        self.pots = [Pot(self.players, min(self.chips.values()))]

        # TODO - the players that should go here are the ones who at the beginning of a BETTING ROUND, they have
        # TODO - more chips than the sum of the maximums of the pots.
        self.eligibles = self.players
        self.update_eligibles()


        self.minimum_bet = 0
        self.set_min()

        self.current_bet = 0
        self.bets = {player: 0 for player in self.players}
        self.winnings = {player: 0 for player in self.players}

    def options(self, player):
        opts = []
        if self.chips[player] > self.current_bet:
            opts.append('CHECK')
            opts.append('RAISE')
            # opts.append('RAISE UP TO ' + str(self.chips[player] - self.current_bet) + ' CHIPS')
            opts.append('FOLD')

        elif self.chips[player] == self.current_bet:
            opts.append('CHECK')
            opts.append('FOLD')

        else:
            opts.append('CHECK')
            opts.append('FOLD')

        return opts

    ''' This method does exactly what it says, bets. No more, no less. Raises need to be dealt with separately,
        game flow needs to be dealt with separately.

        Note that we will take extra care to only present the user with valid bet options.
    '''
    def bet(self, player, amount):

        while amount > 0:
            # self.status()
            for pot in self.pots:
                # this needs to remain really updated
                self.update_eligibles()


                # Clause A - if the pot is not maxed and the player hasn't bet his max amount in the current pot
                if not pot.is_maxed and pot.counts[player] < pot.max_per_player:
                    # A.1
                    if pot.counts[player] + amount <= pot.max_per_player:
                        self.chips[player] -= amount
                        pot.counts[player] += amount
                        amount = 0
                        break

                    # A.2 bet more than the current pot
                    elif pot.counts[player] + amount > pot.max_per_player:
                        # update amount to now be the remaining amount not put in a pot
                        bet_in_current_pot = pot.max_per_player - pot.counts[player]
                        amount -= bet_in_current_pot
                        self.chips[player] -= bet_in_current_pot

                        # this is equivalent to 'pot.counts[player] += bet_in_current_pot'
                        pot.counts[player] = pot.max_per_player

                elif pot == self.pots[-1] and (pot.counts[player] == pot.max_per_player or pot.is_maxed) \
                        and len(self.eligibles) >= 1:
                    '''Clause B - the case where all the pots are maxed, but there are still players to make a side pot with
                        If this happens, there will be another iteration through the loop.
                     '''
                    'the player with the fewest chips that can still enter the side pot determines a lot about it'

                    eligible_players_dict = {player: player.chips for player, chips in self.chips.items()
                                             if player in self.eligibles}
                    key_player = min(eligible_players_dict, key=eligible_players_dict.get)

                    '''the max amount for the new side pot is basically the number of chips the key player will have
                       left over after he bets as much as he can in the current pot
                    '''
                    new_max = key_player.chips - sum([pot.max_per_player for pot in self.pots])
                    new_pot = Pot(self.eligibles, new_max)
                    self.pots.append(new_pot)



    # This method is just for testing
    def bet_tester(self, players_dict, bets):
        self.players = players_dict.keys()
        self.chips = players_dict

        ''' bets is of the form {A:150, B:150, C:100}, to simulate a betting round.
        '''
        self.status()
        for player, amount in bets.items():
            self.bet(player, amount)

        self.status()

    # For testing only
    def status(self):
        num = 1
        for pot in self.pots:
            if pot == self.pots[0]:
                print("Main pot: ")
                print(pot)
                print()
            else:
                print("Side pot " + str(num) + ": ")
                print(pot)
                print()
                num += 1
        print("Chip count - ")
        pprint({player.name: chips for player, chips in self.chips.items()})
        print()

    def is_valid_bet(self, player, amount):
        # if the player has enough to match the current bet and doesn't bet more than he has
        if self.chips[player] >= self.current_bet and amount <= self.chips[player]:
            return True

        # he doesn't have enough to match the current bet, but he is betting all he can
        elif self.chips[player] < self.current_bet and self.chips[player] == amount:
            return True

        else:
            return False

    def can_raise(self, player):
        return self.chips[player] > self.current_bet

    def done_by_fold(self):
        fold_summary = [player.folded for player in self.players]

        # if there is only one player who has still not folded
        return False in [x for x in set(fold_summary) if fold_summary.count(x) == 1]

    @staticmethod
    def pot_folded(pot):
        fold_summary = [player.folded for player in pot.players]

        # if there is only one player who has still not folded
        return False in [x for x in set(fold_summary) if fold_summary.count(x) == 1]

    ''' The below method simulates a betting round. This is the hardest thing to simulate. Here is the logic:

        - if everyone but one player has folded, stop.


    Note - a lot of the crap in this method is dealing with user input, which will be more complex and complete
           when we do the GUI.

    '''
    # # ********************************* Warning - this function is not ideal.. **************************************
    # # command line betting round, if we make a gui, we'd make it in a controller. Note that I'm not going be too
    # # robust with this because we're going to wire it up soon anyway. It's just a proof of concept kind of thing
    def cl_betting_round(self, preflop=False):
        if self.done_by_fold(): pass
        print("Starting betting...")

        matched_raise = {player: True for player in self.players}
        for player in self.players:
            if self.done_by_fold(): break
            if not player.folded:
                print('Hi ' + str(player.name) + '. Your cards are:')
                player.hand.show()

                valid_bet, fold = False, False
                while not valid_bet and not fold:
                    if preflop and player == self.players[0]:
                        # I only want to print this for the first player...
                        print("This is the first betting round. To bet the minimum of " + str(self.minimum_bet) +
                              ", type CHECK.")
                    else:
                        print("Current bet: " + str(self.current_bet) + " chips")

                    inp = input('\n Enter \"CHECK\" to check or call, \"RAISE\" to raise, and \"FOLD\" to fold. If ' +
                                 'you would like to see your particular options, type \"OPTIONS\".')

                    # assure that if the player enters a bad option, they won't be passed into a clause they shouldn't
                    if inp.upper() not in self.options(player): inp = 'nonsense'
                    if inp.upper() == 'CHECK':
                        if preflop:
                            if self.chips[player] > self.minimum_bet:
                                amount = max(self.minimum_bet, self.current_bet)
                            else:
                                amount = self.chips[player]
                        else:
                            amount = self.current_bet

                        # if they can't match the current bet
                        if not self.is_valid_bet(player, amount):
                            amount = self.chips[player]

                        self.bet(player, amount)
                        valid_bet = True
                        self.current_bet = max(amount, self.current_bet)
                        matched_raise[player] = True
                        # valid_bet = self.is_valid_bet(player, amount)

                    elif inp.upper() == 'RAISE':
                        if preflop and self.current_bet == 0:
                            self.current_bet = self.minimum_bet

                        # could be in can_raise
                        if not self.can_raise(player):
                            print("It seems you don't have enough to raise, pick another option.")
                            pass

                        raise_amount = 0
                        while not valid_bet and self.can_raise(player):
                            raise_amount = int(input('The current bet is ' + str(self.current_bet) + ' chips. Enter by how ' +
                                                    'much would you like to raise it:'))
                            valid_bet = self.is_valid_bet(player, self.current_bet + raise_amount)

                        matched_raise = {player: False for player in self.players}
                        matched_raise[player] = True
                        self.current_bet += raise_amount
                        self.bet(player, self.current_bet)


                    elif inp.upper() == 'FOLD':
                        player.fold()
                        fold = True

                    elif inp.upper() == 'OPTIONS':
                        for option in self.options(player): print(option)

                    else:
                        # There must have been bad input, they'll have to try again!
                        pass

        for player in self.players:
            if self.done_by_fold(): break
            if not matched_raise[player]:
                input_invalid = True
                while input_invalid:
                    inp = input(str(player.name) + "! Would you like to match the current bet of " +
                                str(self.current_bet) +
                                "? You've already put in " + str(self.bets[player]) + ", so it will require " +
                                "either " + str(self.current_bet - self.bets[player]) + ", or all your chips," +
                                " whichever is smaller." +
                                " Type 'yes' to fight on, 'no' to fold:")
                    if inp.upper() == 'YES':
                        # add the additional amount to their bet
                        if self.is_valid_bet(player, self.current_bet - self.bets[player]):
                            self.bet(player, self.current_bet - self.bets[player])
                            matched_raise[player] = True

                        # if they can't make the full bet
                        else:
                            # then they'll have to bet the rest of their chips
                            self.bet(player, self.chips[player])
                        input_invalid = False
                    elif inp.upper() == 'NO':
                        player.fold()
                        input_invalid = False
                    else:
                        pass

        # I guess now it's time to test this thing...

    def pot_winner(self, pot):
        # if all the players fold, we don't need to compare cards to see who wins, we just pick the one who
        # hasn't folded yet.
        if BetManager.pot_folded(pot):
            for player in pot.players:
                if not player.folded:
                    return [player]

        for player in pot.players:
            player.best_hand = Hand.get_best_hand(Hand(self.round.community_cards) + player.hand)

        winners = [pot.players[0]]
        best_hand = winners[0].best_hand
        for player in pot.players:
            if Hand.winner(best_hand, player.best_hand) == player.best_hand:
                # if there is a clear winner we need to reset the winners array, because maybe there was a tie
                # between two players and a third player beat one of them (and thus both of them)
                winners = [player]
                best_hand = player.best_hand

            # if there is a tie!
            elif Hand.winner(best_hand, player.best_hand) is None and player not in winners:
                winners.append(player)
            else:
                pass

        return winners

    def distribute(self):
        num = 1
        for pot in self.pots:
            winners = self.pot_winner(pot)
            if len(winners) == 1:
                winner = winners[0]
                winner.chips += pot.get_amount()

                if pot == self.pots[0]:
                    print(winner.name + ' wins the main pot.')
                else:
                    print(winner.name + ' wins side pot ' + str(num))
                    num += 1

            else:
                share = pot.get_amount() / float(len(winners))
                for winner in winners:
                    winner.chips += share
                    print(winner.name)
                if pot == self.pots[0]:
                    print('have won the main pot.')
                else:
                    print(' wins side pot ' + str(num))
                    num += 1

    def reset(self):
        self.minimum_bet = 0
        self.set_min()

        self.current_bet = 0
        self.bets = {player: 0 for player in self.players}  # used in constructor, no need to call elsewhere

    ''' The following are methods that are used internally in this class, and should not be used
        elsewhere.
    '''
    def set_min(self):
        # initialize to some players chip count, a number definitely not smaller than min
        min_chips = self.chips[self.players[0]]
        for amount in self.chips.values():
            min_chips = min(math.ceil(0.5 * amount), self.round.table_min)

        self.minimum_bet = min_chips
        
    # to occur at the beginning of each betting round 
    def update_eligibles(self):
        self.eligibles = [player for player in self.players 
                                if self.chips_at_beginning[player] > sum([pot.max_per_player for pot in self.pots])]
        
        
    


