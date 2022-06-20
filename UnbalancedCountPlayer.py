from BasicStrategyPlayer import BasicStrategyPlayer


class UnbalancedCountPlayer(BasicStrategyPlayer):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.cards_discarded = 0

    # METHODS TO BE OVERRIDDEN IN SUBCLASSES
    def calculate_wager_amount(self):
        pass

    def notify_card(self, card):
        pass

    def notify_shuffle(self):
        pass
