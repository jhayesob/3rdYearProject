from Player import Player


class NeverBustPlayer(Player):
    def __init__(self):
        super().__init__()

    def make_choice(self, dealers_up_card, *args):
        if self.hand.get_hand_value() <= 11:
            return 'h'
        else:
            return 'std'
