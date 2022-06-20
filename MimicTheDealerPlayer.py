from Player import Player


class MimicTheDealerPlayer(Player):
    def __init__(self):
        super().__init__()

    def make_choice(self, dealers_up_card, *args):
        if self.hand.get_hand_value() < 17:
            return 'h'
        else:
            return 'std'
