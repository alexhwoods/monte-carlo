from monte_carlo.components.models.Hand import Hand
from monte_carlo.components.models.Pot import Pot
import math


class BetManager:
    ''' Function summary:
            getOptions(player) - returns betting options for a player
            getRaiseLimit(player) - returns the maximum amount a player can raise
            fold(player)
            bet(player, amount)
            setRaise(player) - used in bet(), simply updates the current bet and who's matched it
            

    TODO - I need a good way of saving the data to a database to use for the machine learning model.


    Wondering if I should make a betting round object...damn betting is complicated.


    TODO: make sure the order in which players are prompted to bet makes sense.
    
    '''

    betting_options = ['CALL', 'CHECK', 'RAISE', 'FOLD']

    def __init__(self, game):
        self.game = game

        # if you don't do .copy() some weird shit happens because of something horrible called "shallow copying"
        self.players = game.players.copy()

        # table is a stack of the players (ok a mini-stack, it's like 15% implemented haha)
        self.table = game.players.copy()

        self.chips = {player: player.chips for player in self.players}
        self.chips_at_beginning = {player: player.chips for player in self.players}
        self.started = False

        # there is initially one pot, namely, the main pot. The max per player is added later
        self.pots = [Pot(self.players, 0)]

        # players eligible to join the next side pot, only used internally
        self.eligibles = self.players.copy()
        self.update_eligibles()

        # only used internally
        self.matched_raise = {player: True for player in self.players}


        self.minimum_bet = 0
        self.set_min()

        self.current_bet = 0
        self.bets = {player: 0 for player in self.players}
        self.winnings = {player: 0 for player in self.players}

    def startBettingRound(self):
        self.started = True
        self.pots[0].max_per_player = min(self.chips.values())

        self.current_bet = 0
        self.matched_raise = {player: False for player in self.players if not player.folded}

    def getOptions(self, player):
        opts = []
        if self.chips[player] > self.current_bet:
            opts.append('CHECK')
            opts.append('RAISE')
            opts.append('FOLD')

        elif self.chips[player] == self.current_bet:
            opts.append('CHECK')
            opts.append('FOLD')

        else:
            opts.append('CHECK')
            opts.append('FOLD')

        return opts
    
    def getRaiseLimit(self, player):
        if 'RAISE' not in self.getOptions(player):
            return None
        else:
            return self.chips[player] - self.current_bet

    def getPots(self):
        if not self.started:
            return "Betting Round Not Started."
        else:
            return self.pots
        
    def fold(self, player):
        player.fold()

        # in case the fold request is sent too many times (a player should only be able to fold once per round)
        if player in self.table:
            self.table.remove(player)

    def nextBetter(self):
        if not self.started:
            return "Betting Round Not Started."
        else:
            if self.done_by_fold():
                return None

            for player in self.table:
                if not player.folded and not self.matched_raise[player]:
                    return player

            return None

    # for internal testing purposes, but might be useful in the future.
    def getBetStatus(self):
        summary = {}
        for player in self.table:
            already_bet = sum([pot.counts[player] for pot in self.pots if player in pot.players])
            summary[player] = already_bet

        return summary

    ''' This method does exactly what it says, bets. No more, no less. Raises need to be dealt with separately,
        game flow needs to be dealt with separately.

        Note that we will take extra care to only present the user with valid bet options.
    '''
    def bet(self, player, amount, is_raise=False):

        if is_raise:
            print("RAISE WAS SET, MATCHED RAISE UPDATED.")
            self.setRaise(player)
            self.current_bet = amount

        already_bet = sum([pot.counts[player] for pot in self.pots if player in pot.players])
        # print(self.getBetStatus())

        # print("Value to contest: " + str(already_bet + amount))
        if amount == self.current_bet or player.chips - amount == 0 or already_bet + amount == self.current_bet:
            print("PLAYER RAISE STATUS UPDATED.")
            self.matched_raise[player] = True

            # move the player who just bet to the back of the stack
            self.table.append(self.table.pop(0))

        while amount > 0:
            for pot in self.pots:
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



    # internal
    def setRaise(self, player):
        self.matched_raise = {player: False for player in self.table}
        self.matched_raise[player] = True

    # internal
    def pot_folded(self, pot):
        fold_summary = []
        if pot in self.pots:
            fold_summary = [player.folded for player in pot.players]

            # if there is only one player who has still not folded
            return False in [x for x in set(fold_summary) if fold_summary.count(x) == 1]

        else:
            return None

    # internal, pot stuff is internal
    def getPotWinner(self, pot):
        # if all the players fold, we don't need to compare cards to see who wins, we just pick the one who
        # hasn't folded yet.
        if self.pot_folded(pot):
            for player in pot.players:
                if not player.folded:
                    return [player]

        for player in pot.players:
            if player.hand is None:
                # if they haven't dealt yet
                return None

            round = self.game.getCurrentRound()
            if round.stage == 'HOLE':
                # if still in the hole stage, no community cards have been dealt, but you can still discern a winner
                player.best_hand = player.hand
            else:
                player.best_hand = Hand.get_best_hand(Hand(round.community_cards) + player.hand)

        winners = [pot.players[0]]
        best_hand = winners[0].best_hand
        for player in list(set(pot.players).intersection(set(self.table))):
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

    def getAllWinners(self):
        dict = {pot: [] for pot in self.pots}
        for pot in self.pots:
            dict[pot] = self.getPotWinner(pot)

        raise_status = self.getRaiseStatus()
        if False in raise_status.values():
            return None
        else:
            return dict

    def getRaiseStatus(self):
        return self.matched_raise

    def getPotStatus(self):
        return [pot.counts for pot in self.pots]

    def getFoldStatus(self):
        return {player: player.folded for player in self.players}

    # internal UE
    def distribute(self):
        for pot in self.pots:
            winners = self.getPotWinner(pot)
            if winners is None:
                pass
            elif len(winners) == 1:
                winner = winners[0]
                winner.chips += pot.get_amount()

            else:
                share = pot.get_amount() / float(len(winners))
                for winner in winners:
                    winner.chips += share



    # internal, NUE (not used elsewhere)
    def done_by_fold(self):
        fold_summary = [player.folded for player in self.players]

        # if there is only one player who has still not folded
        return False in [x for x in set(fold_summary) if fold_summary.count(x) == 1]

    # internal, UE (used elsewhere)
    def reset(self):
        self.minimum_bet = 0
        self.set_min()

        self.current_bet = 0

    # internal and stays in this class
    def set_min(self):
        # initialize to some players chip count, a number definitely not smaller than min
        if len(self.players) > 0:
            min_chips = self.chips[self.players[0]]
        else:
            min_chips = 0
        for amount in self.chips.values():
            min_chips = min(math.ceil(0.5 * amount), self.game.table_min)

        self.minimum_bet = min_chips

    # internal and within class only (to occur at the beginning of each betting round)
    def update_eligibles(self):
        self.eligibles = [player for player in self.players
                          if self.chips_at_beginning[player] > sum([pot.max_per_player for pot in self.pots])]

    # internal
    def is_valid_bet(self, player, amount):
        # if the player has enough to match the current bet and doesn't bet more than he has
        if self.chips[player] >= self.current_bet and amount <= self.chips[player]:
            return True

        # he doesn't have enough to match the current bet, but he is betting all he can
        elif self.chips[player] < self.current_bet and self.chips[player] == amount:
            return True

        else:
            return False
        






    


