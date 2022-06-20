from BasicStrategyPlayer import BasicStrategyPlayer
from math import trunc


class BalancedCountPlayer(BasicStrategyPlayer):
    # all card counting classes without deviations inherit methods from BasicStrategyPlayer for all
    # decisions other than betting
    def __init__(self, bet_spread):
        super().__init__()
        self.bet_spread = bet_spread
        self.count = 0
        self.cards_discarded = 0

    def calculate_wager_amount(self):  # '1_to_8_bet_spread' || '1_to_12_bet_spread'
        if self.bet_spread == '1_to_8_bet_spread':
            # BET SPREAD OF 1 TO 8
            # ONE UNIT AT TC: +1
            # TWO UNITS AT TC: +2
            # FOUR UNITS AT TC: +3
            # EIGHT UNITS AT TC: +4 AND ABOVE
            if self.true_count <= 1:
                return self.betting_unit_value
            elif self.true_count == 2:
                return self.betting_unit_value * 2
            elif self.true_count == 3:
                return self.betting_unit_value * 4
            elif self.true_count >= 4:
                return self.betting_unit_value * 8

        elif self.bet_spread == '1_to_12_bet_spread':
            if self.true_count <= 1:
                return self.betting_unit_value
            elif self.true_count == 2:
                return self.betting_unit_value * 3
            elif self.true_count == 3:
                return self.betting_unit_value * 6
            elif self.true_count >= 4:
                return self.betting_unit_value * 12

    # METHOD TO BE OVERRIDDEN IN SUBCLASSES
    def notify_card(self, card):
        pass

    def notify_shuffle(self):
        self.count = 0
        self.cards_discarded = 0

    @staticmethod
    def decks_remaining(n):
        if 0 <= n < 39:
            return 0.5
        elif 39 <= n < 65:
            return 1
        elif 65 <= n < 91:
            return 1.5
        elif 91 <= n < 117:
            return 2
        elif 117 <= n < 143:
            return 2.5
        elif 143 <= n < 169:
            return 3
        elif 169 <= n < 195:
            return 3.5
        elif 195 <= n < 221:
            return 4
        elif 221 <= n < 247:
            return 4.5
        elif 247 <= n < 273:
            return 5
        elif 273 <= n < 299:
            return 5.5
        elif 299 <= n < 313:
            return 6
        # only accurate to the closest 1/2 of a deck, as real players won't be able to have more accuracy than that

    @property
    def true_count(self):
        return trunc(self.count / self.decks_remaining(312 - self.cards_discarded))
