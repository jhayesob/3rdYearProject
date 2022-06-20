from Hand import Hand


class Dealer:
    def __init__(self):
        self.hand = Hand()

    def make_choice(self):
        if self.hand.get_hand_value() < 17:
            return 'hit'
        else:
            return 'std'
