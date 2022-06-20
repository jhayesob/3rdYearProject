from Hand import Hand
from ListTree import ListTree


class Player:
    def __init__(self):
        self.hand = Hand()
        self.split_hands = ListTree()
        self.bank_roll = 10000  # betting slider of 1 to 8 units: £10 each
        self.betting_unit_value = 10

    def calculate_wager_amount(self):
        return self.betting_unit_value

    # UNUSED METHOD
    def post_wager(self, amount):
        self.bank_roll -= amount
        return amount

    # UNUSED METHOD
    def receive_payout(self, p):
        self.bank_roll += p
        pass

    # UNUSED METHOD
    def decide_take_even_money(self):
        return False

    # METHOD TO BE OVERRIDDEN IN SUBCLASSES
    def notify_card(self, card):
        pass

    # METHOD TO BE OVERRIDDEN IN SUBCLASSES
    def notify_shuffle(self):
        pass

    # METHOD TO BE OVERRIDDEN IN SUBCLASSES
    def decide_take_insurance(self):
        # if dealer has a blackjack, you've protected yourself but forfeited up
        # to half the value of your bet in the process.
        return False

    def post_insurance_bet(self, player_wager):
        # players can have a choice of betting anywhere up to half the value of their current wager
        # this function is coded to bet the maximum insurance wager as is insurance is only chosen
        # when the true count is >= 3 and the probable outcomes are favourable.
        if player_wager != 0:
            bet = player_wager * 0.5
            # self.bank_roll -= bet
            return bet
        else:
            return 0

    def make_choice(self, dealers_up_card, *args):
        pass
