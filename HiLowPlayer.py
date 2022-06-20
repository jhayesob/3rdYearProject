from BalancedCountPlayer import BalancedCountPlayer
from BasicStrategyPlayer import BasicStrategyPlayer
from Card import CardFace


class HiLowPlayer(BalancedCountPlayer):
    # card counting class inherits methods from basic strategy class for all
    # playing decisions other than betting

    def __init__(self, bet_spread):
        super().__init__(bet_spread)
        self.count_scheme = {
            CardFace.ACE: -1,
            CardFace.KING: -1,
            CardFace.QUEEN: -1,
            CardFace.JACK: -1,
            CardFace.TEN: -1,
            CardFace.NINE: 0,
            CardFace.EIGHT: 0,
            CardFace.SEVEN: 0,
            CardFace.SIX: 1,
            CardFace.FIVE: 1,
            CardFace.FOUR: 1,
            CardFace.THREE: 1,
            CardFace.TWO: 1,
        }

    def notify_card(self, card):
        self.count += self.count_scheme[card.face]
        self.cards_discarded += 1

    def get_tc(self):
        return self.true_count


class HiLowDeviationsPlayer(HiLowPlayer):
    def __init__(self, bet_spread):
        super().__init__(bet_spread)

    @property
    def decide_take_insurance(self):
        if self.true_count >= 3.0:
            return True
        else:
            return False

    def make_choice(self, dealers_up_card, *args):
        # determine to stand, hit, split or d-down and return associated char
        # args[0] should be used to pass in the index of the Hand in question when there are split hands in play.
        if len(args) == 0:
            deviation = deviation_cases(self.hand, dealers_up_card, self.true_count)
            if deviation != 'n':
                return deviation
            else:
                if self.hand.is_pair():
                    if BasicStrategyPlayer.should_be_split(self.hand.cards[0].face, dealers_up_card):
                        return 'split'
                    else:
                        return BasicStrategyPlayer.hard_totals(self.hand, dealers_up_card)
                elif self.hand.soft:
                    return BasicStrategyPlayer.soft_totals(self.hand, dealers_up_card)
                else:
                    return BasicStrategyPlayer.hard_totals(self.hand, dealers_up_card)
        else:
            deviation = deviation_cases(self.split_hands[args[0]], dealers_up_card, self.true_count)
            if deviation != 'n':
                return deviation
            else:
                if self.split_hands[args[0]].is_pair() and not self.split_hands[args[0]].splitFromAces and \
                        self.split_hands[args[0]].num_splits < 3:
                    if BasicStrategyPlayer.should_be_split(self.split_hands[args[0]].cards[0].face, dealers_up_card):
                        return 'split'
                    else:
                        return BasicStrategyPlayer.hard_totals(self.split_hands[args[0]], dealers_up_card)
                elif self.hand.soft:
                    return BasicStrategyPlayer.soft_totals(self.split_hands[args[0]], dealers_up_card)
                else:
                    return BasicStrategyPlayer.hard_totals(self.split_hands[args[0]], dealers_up_card)


def deviation_cases(hand, dealers_up_card, t_count):
    if hand.get_hand_value() == 16 and dealers_up_card.face == CardFace.TEN and t_count >= 0:
        return 'std'
    elif hand.get_hand_value() == 15 and dealers_up_card.face == CardFace.TEN and t_count >= 4:
        return 'std'
    elif hand.is_pair() and hand.cards[0].face == CardFace.TEN and dealers_up_card.face == CardFace.FIVE and t_count >=\
            5:
        return 'split'
    elif hand.is_pair() and hand.cards[0].face == CardFace.TEN and dealers_up_card.face == CardFace.SIX and t_count >=\
            4:
        return 'split'
    else:
        return 'n'
