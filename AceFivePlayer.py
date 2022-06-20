from BalancedCountPlayer import BalancedCountPlayer
from Card import CardFace


class AceFivePlayer(BalancedCountPlayer):
    # card counting class inherits methods from basic strategy class for all
    # playing decisions other than betting

    def __init__(self, bet_spread):
        super().__init__(bet_spread)
        self.count_scheme = {
            CardFace.ACE: -1,
            CardFace.KING: 0,
            CardFace.QUEEN: 0,
            CardFace.JACK: 0,
            CardFace.TEN: 0,
            CardFace.NINE: 0,
            CardFace.EIGHT: 0,
            CardFace.SEVEN: 0,
            CardFace.SIX: 0,
            CardFace.FIVE: 1,
            CardFace.FOUR: 0,
            CardFace.THREE: 0,
            CardFace.TWO: 0,
        }

    def notify_card(self, card):
        self.count += self.count_scheme[card.face]
        self.cards_discarded += 1
