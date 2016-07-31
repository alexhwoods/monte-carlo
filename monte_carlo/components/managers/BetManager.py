from monte_carlo.components.models.Player import Player
from collections import namedtuple
import math

# these things fucking rock, it's like a baby object
Surplus = namedtuple('Surplus', ['player', 'amount'])


class BetManager(object):

    betting_options = ['CALL', 'CHECK', 'RAISE', 'FOLD']

    def __init__(self, round):
        self.round = round
        self.players = round.players
        self.chips = {player: player.chips for player in self.players}
        self.pot = 0

        self.minimum_bet = 0
        self.set_min()

        self.current_bet = 0
        self.bets = {player: 0 for player in self.players}
        self.winnings = {player: 0 for player in self.players}

    def options(self, player):
        opts = []
        if self.chips[player] > self.current_bet:
            opts.append('CHECK')
            opts.append('RAISE UP TO ' + str(self.chips[player] - self.current_bet) + ' CHIPS')
            opts.append('FOLD')

        elif self.chips[player] == self.current_bet:
            opts.append('CHECK, WHICH FOR YOU IS ALL-IN')
            opts.append('FOLD')

        else:
            opts.append('CHECK, WHICH FOR YOU IS ALL-IN. AND IF YOU WIN, YOU CAN\'T WIN THE WHOLE POT')
            opts.append('FOLD')

        return opts

    # used in constructor, no need to call elsewhere
    def set_min(self):
        # initialize to some players chip count, a number definitely not smaller than min
        min_chips = self.chips[self.players[0]]
        for amount in self.chips.values():
            min_chips = min(math.ceil(0.5*amount), self.round.table_min)

        self.minimum_bet = min_chips

    def bet(self, player, amount):
        player.chips = player.chips - amount
        self.chips[player] = player.chips

        # we have to just add the amount because there are 3 betting rounds.
        self.bets[player] += amount

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

    # if the betting is done, and the winner is set, we need to handle any surpluses that are due
    def handle_surplus(self):
        surpluses = []

        if self.round.winners is not None:
            min_winning_bet = min([bet for player, bet in self.bets if player in self.round.winners])
            # if the winner didn't make the maximum bet (then surpluses are needed)
            if min_winning_bet != max(self.bets.values()):
                for player in self.players:
                    # create a surplus of the extra amount the player put into the pot
                    temp = Surplus(player, self.bets[player] - min_winning_bet)
                    surpluses.append(temp)
                    self.winnings[player] = temp.amount
                    self.pot -= temp.amount

            # this is if the winner of the round meet all the current bets
            else:
                pass

        # "refunding" the over-betters
        if len(surpluses) > 0:
            for surplus in surpluses: surplus.player.chips += surplus.amount

    def get_pot(self):
        self.pot = sum(self.bets.values())
        return self.pot

    def done_by_fold(self):
        fold_summary = [player.folded for player in self.players]

        # if there is only one player who has still not folded
        return False in [x for x in set(fold_summary) if fold_summary.count(x) == 1]


    # ********************************* Warning - this function is a bitch **************************************
    # command line betting round, if we make a gui, we'd make it in a controller. Note that I'm not going be too
    # robust with this because we're going to wire it up soon anyway. It's just a proof of concept kind of thing
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

                        if not self.can_raise(player):
                            print("It seems you don't have enough to raise, pick another option.")
                            pass

                        raise_amount = 0
                        while not valid_bet:
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

    def get_winnings(self):
        # this function assumes self.handle_surplus() has already been run

        winners = self.round.get_winner()
        if len(winners) == 1:
            self.winnings[winners[0]] = self.get_pot()

        else:
            share = self.get_pot() / len(winners)
            for player in winners:
                self.winnings[player] = share

        return self.winnings

    def reset(self):
        self.pot = 0
        self.minimum_bet = 0
        self.set_min()

        self.current_bet = 0
        self.bets = {player: 0 for player in self.players}


