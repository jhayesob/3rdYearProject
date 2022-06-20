from UnbalancedCountPlayer import UnbalancedCountPlayer
from Card import CardFace


class KOPlayer(UnbalancedCountPlayer):
    # card counting class inherits methods from basic strategy class for all
    # playing decisions other than betting

    def __init__(self):
        super().__init__()
        self.count_scheme = {
            CardFace.ACE: -1,
            CardFace.KING: -1,
            CardFace.QUEEN: -1,
            CardFace.JACK: -1,
            CardFace.TEN: -1,
            CardFace.NINE: 0,
            CardFace.EIGHT: 0,
            CardFace.SEVEN: 1,
            CardFace.SIX: 1,
            CardFace.FIVE: 1,
            CardFace.FOUR: 1,
            CardFace.THREE: 1,
            CardFace.TWO: 1,
        }

    def calculate_wager_amount(self):
        if self.count <= -2:
            return self.betting_unit_value
        elif self.count == -1:
            return self.betting_unit_value * 2
        elif self.count == 0:
            return self.betting_unit_value * 3
        elif self.count == 1:
            return self.betting_unit_value * 4
        elif self.count == 2:
            return self.betting_unit_value * 5
        elif self.count == 3:
            return self.betting_unit_value * 6
        elif self.count == 4:
            return self.betting_unit_value * 7
        elif self.count >= 5:
            return self.betting_unit_value * 8

    def notify_card(self, card):
        self.count += self.count_scheme[card.face]
        self.cards_discarded += 1

    def notify_shuffle(self):
        self.count = -20
        self.cards_discarded = 0
