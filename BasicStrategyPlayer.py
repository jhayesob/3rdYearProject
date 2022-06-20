import Card
from Card import CardFace
from Player import Player

pair_splitting = {
    # Depending on dealer's up card. In order [2,3,4,5,6,7,8,9,10,A]
    CardFace.ACE: [True] * 10,
    CardFace.KING: [False] * 10,
    CardFace.QUEEN: [False] * 10,
    CardFace.JACK: [False] * 10,
    CardFace.TEN: [False] * 10,
    CardFace.NINE: [True] * 5 + [False] + [True] * 2 + [False] * 2,
    CardFace.EIGHT: [True] * 10,
    CardFace.SEVEN: [True] * 6 + [False] * 4,
    CardFace.SIX: [True] * 5 + [False] * 5,
    CardFace.FIVE: [False] * 10,
    CardFace.FOUR: [False] * 3 + [True] * 2 + [False] * 5,
    CardFace.THREE: [True] * 6 + [False] * 4,
    CardFace.TWO: [True] * 6 + [False] * 4
}

assert all([len(v) == 10 for (_, v) in pair_splitting.items()])

soft_two_card_totals = {
    20: ['std'] * 10,
    19: ['std'] * 4 + ['dd'] + ['std'] * 5,
    18: ['dd'] * 5 + ['std'] * 2 + ['h'] * 3,
    17: ['h'] + ['dd'] * 4 + ['h'] * 5,
    16: ['h'] * 2 + ['dd'] * 3 + ['h'] * 5,
    15: ['h'] * 2 + ['dd'] * 3 + ['h'] * 5,
    14: ['h'] * 3 + ['dd'] * 2 + ['h'] * 5,
    13: ['h'] * 3 + ['dd'] * 2 + ['h'] * 5,
    12: ['h'] * 3 + ['std'] * 2 + ['h'] * 5,
}

assert all([len(v) == 10 for (_, v) in soft_two_card_totals.items()])

soft_totals = {
    20: ['std'] * 10,
    19: ['std'] * 4 + ['h'] + ['std'] * 5,
    18: ['std'] * 7 + ['h'] * 3,
    17: ['h'] * 10,
    16: ['h'] * 10,
    15: ['h'] * 10,
    14: ['h'] * 10,
    13: ['h'] * 10,
    12: ['h'] * 3 + ['std'] * 2 + ['h'] * 5,
}

assert all([len(v) == 10 for (_, v) in soft_totals.items()])

hard_two_card_totals = {
    17: ['std'] * 10,
    16: ['std'] * 5 + ['h'] * 5,
    15: ['std'] * 5 + ['h'] * 5,
    14: ['std'] * 5 + ['h'] * 5,
    13: ['std'] * 5 + ['h'] * 5,
    12: ['h'] * 2 + ['std'] * 3 + ['h'] * 5,
    11: ['dd'] * 10,
    10: ['dd'] * 8 + ['h'] * 2,
    9: ['h'] + ['dd'] * 4 + ['h'] * 5,
    8: ['h'] * 10,
    7: ['h'] * 10,
    6: ['h'] * 10,
    5: ['h'] * 10,
    4: ['h'] * 10,
}

assert all([len(v) == 10 for (_, v) in hard_two_card_totals.items()])

hard_totals = {
    17: ['std'] * 10,
    16: ['std'] * 5 + ['h'] * 5,
    15: ['std'] * 5 + ['h'] * 5,
    14: ['std'] * 5 + ['h'] * 5,
    13: ['std'] * 5 + ['h'] * 5,
    12: ['h'] * 2 + ['std'] * 3 + ['h'] * 5,
    11: ['h'] * 10,
    10: ['h'] * 10,
    9: ['h'] * 10,
    8: ['h'] * 10,
    7: ['h'] * 10,
    6: ['h'] * 10,
    5: ['h'] * 10,
    4: ['h'] * 10,
}

assert all([len(v) == 10 for (_, v) in hard_totals.items()])

up_card_row_list = list(range(2, 11 + 1))
up_card_row_dict = dict(zip(up_card_row_list, list(range(len(up_card_row_list)))))


# class BasicStrategyPlayer acts is extended by different card counting classes.
# subclasses will have to be passed card count parameters (to specify what state their card counts are in) in order to
# make decisions as well as the GAME parameters that are passed to BasicStrategyPlayer.

def basic_strategy_test_harness():
    hands_tuple = Card.make_two_card_hands_tuple() + Card.make_three_card_hands_tuple()
    # print(f"length of hands_tuple = {len(hands_tuple)}")
    # for each card combo put all dealer up cards in combos with them
    keys_tuple = ()
    for i in hands_tuple:
        for j in ('2', '3', '4', '5', '6', '7', '8', '9', 't', 'a'):
            keys_tuple = keys_tuple + ((i, j),)
    print(keys_tuple)
    response_dictionary = {}
    for j in range(len(keys_tuple)):
        response_dictionary[keys_tuple[j]] = alt_make_choice(keys_tuple[j])
    for key, value in response_dictionary.items():
        # print(key, '->', value)
        player = BasicStrategyPlayer()
        # print(f"key[0] = {key[0]}")
        for i in range(len(key[0])):
            card = None
            if key[0][i] in ['2', '3', '4', '5', '6', '7', '8', '9']:
                card = Card.Card(Card.Suit.DIAMONDS, CardFace(int(key[0][i])))
            elif key[0][i] in ['t', 'j', 'q', 'k']:
                card = Card.Card(Card.Suit.DIAMONDS, CardFace.TEN)
            else:
                card = Card.Card(Card.Suit.DIAMONDS, CardFace.ACE)
            player.hand.add_to_hand(card)
        d_up_card = None
        if key[1] in ['2', '3', '4', '5', '6', '7', '8', '9']:
            d_up_card = Card.Card(Card.Suit.DIAMONDS, CardFace(int(key[1])))
        elif key[1] in ['t', 'j', 'q', 'k']:
            d_up_card = Card.Card(Card.Suit.DIAMONDS, CardFace.TEN)
        else:
            d_up_card = Card.Card(Card.Suit.DIAMONDS, CardFace.ACE)
        response = player.make_choice(d_up_card)
        if response != value:
            print(f"issue at: {key} | response = {response} | correct response = {value}")
    # print(f"if no strings just came up saying 'issue at: ...', then you're in the clear")


def alt_make_choice(key):
    hand = key[0]
    card_vals = []
    for i in range(len(hand)):
        card_vals.append(0)
    # CODE REUSE: outline initial matrix of card values based on card face enums
    n = 0
    for i in hand:
        if i in ['2', '3', '4', '5', '6', '7', '8', '9']:
            card_vals[n] = int(i)
        elif i in ['t', 'j', 'q', 'k']:
            card_vals[n] = 10
        else:
            card_vals[n] = 11
        n += 1

    # count number of aces present
    num_aces = hand.count('a')

    all_aces_converted = False
    if num_aces == 0:
        all_aces_converted = True

    # convert values of aces in bust hands to 1 while hand is bust
    i = 0
    num_aces_converted = 0
    while (not all_aces_converted) and sum(card_vals) > 21:
        if hand[i] == 'a':
            card_vals[i] = 1
            num_aces_converted += 1
            if num_aces == num_aces_converted:
                all_aces_converted = True
        i += 1

    if len(hand) == 2 and hand[0] == hand[1]:
        # pair values logic
        if hand[0] in ['a', '8']:
            return "split"
        elif hand[0] == '9' and key[1] not in ['7', 't', 'a']:
            return "split"
        elif hand[0] == '7' and key[1] not in ['8', '9', 't', 'a']:
            return "split"
        elif hand[0] == '6' and key[1] not in ['7', '8', '9', 't', 'a']:
            return "split"
        elif hand[0] == '4' and key[1] in ['5', '6']:
            return "split"
        elif hand[0] in ['2', '3'] and key[1] not in ['8', '9', 't', 'a']:
            return "split"
        else:
            return alt_hard_totals(card_vals, key[1])
    elif 11 in card_vals:
        # soft hand logic
        # isolate away the ace valued at 1 and count up the other values
        other_val = sum(card_vals) - 11
        if (other_val in [9, 10]) or (other_val == 8 and key[1] != '6') or (other_val == 7 and key[1] in ['7', '8']):
            return 'std'
        if (other_val == 8 and key[1] == '6') or (other_val == 6 and key[1] in ['3', '4', '5', '6']) or \
                (other_val in [4, 5] and key[1] in ['4', '5', '6']) or (
                other_val in [2, 3] and key[1] in ['5', '6']):
            if len(hand) == 2:
                return 'dd'
            else:
                return 'h'
        elif other_val == 7 and key[1] in ['2', '3', '4', '5', '6']:
            if len(hand) == 2:
                return 'dd'
            else:
                return 'std'
        else:
            return 'h'
    else:
        # hard hands logic
        return alt_hard_totals(card_vals, key[1])


def alt_hard_totals(card_vals, d_up_card):
    # print(f"card vals = {card_vals} || dUp : {d_up_card}")
    if (sum(card_vals) >= 17) or (sum(card_vals) in [16, 15, 14, 13] and d_up_card in ['2', '3', '4', '5', '6']) or \
            (sum(card_vals) == 12 and d_up_card in ['4', '5', '6']):
        return 'std'
    elif len(card_vals) == 2:
        if (sum(card_vals) == 11) or (sum(card_vals) == 10 and d_up_card in ['2', '3', '4', '5', '6', '7', '8', '9']) \
                or (sum(card_vals) == 9 and d_up_card in ['3', '4', '5', '6']):
            return 'dd'
        else:
            return 'h'
    else:
        return 'h'


class BasicStrategyPlayer(Player):
    def __init__(self):
        super().__init__()

    def make_choice(self, dealers_up_card, *args):
        # determine to stand, hit, split or d-down and return associated char
        # args[0] should be used to pass in the index of the Hand in question when there are split hands in play.
        if len(args) == 0:
            if self.hand.is_pair():
                if BasicStrategyPlayer.should_be_split(self.hand.cards[0].face, dealers_up_card):
                    return 'split'
                else:
                    return BasicStrategyPlayer.hard_totals(self.hand, dealers_up_card)
            elif self.hand.is_soft():
                return BasicStrategyPlayer.soft_totals(self.hand, dealers_up_card)
            else:
                return BasicStrategyPlayer.hard_totals(self.hand, dealers_up_card)
        else:
            if self.split_hands[args[0]].is_pair() and not self.split_hands[args[0]].splitFromAces and \
                    self.split_hands[args[0]].num_splits < 3:
                if BasicStrategyPlayer.should_be_split(self.split_hands[args[0]].cards[0].face, dealers_up_card):
                    return 'split'
                else:
                    return BasicStrategyPlayer.hard_totals(self.split_hands[args[0]], dealers_up_card)
            elif self.hand.is_soft():
                return BasicStrategyPlayer.soft_totals(self.split_hands[args[0]], dealers_up_card)
            else:
                return BasicStrategyPlayer.hard_totals(self.split_hands[args[0]], dealers_up_card)

    @staticmethod
    def should_be_split(card_face, d):
        x = pair_splitting[card_face]
        y = up_card_row_dict[d.value]
        try:
            z = x[y]
            return z
        except IndexError:
            print(f"offending index was {y}")

    @staticmethod
    def soft_totals(h, d):
        assert any([card.face == CardFace.ACE for card in h.cards])
        hand_val = h.get_hand_value()
        if hand_val > 20:
            return 'std'
        else:
            if len(h.cards) == 2:
                x = soft_two_card_totals[hand_val]
            else:
                x = soft_totals[hand_val]
            y = up_card_row_dict[d.value]
            z = x[y]
            return z

    @staticmethod
    def hard_totals(h, d):
        hand_val = h.get_hand_value()
        if hand_val > 17:
            return 'std'
        else:
            if len(h.cards) == 2:
                x = hard_two_card_totals[hand_val]
            else:
                x = hard_totals[hand_val]
            y = up_card_row_dict[d.value]
            z = x[y]
            return z
