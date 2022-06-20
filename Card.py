from enum import Enum


def card_testing():
    # card class needs to be able to provide every kind of card in a 52 deck of
    # cards and a cut card.
    # ** instantiate every necessary type of card.
    valid = True
    for i in Suit:
        for o in CardFace:
            c = Card(i, o)
            # validate normal cards
            if c.suit.value != i.value or c.face.value != o.value:
                valid = False
                print("failed at real cards")
            print(str(c.suit.value) + " " + str(c.face.value) + " _vs_ " + str(i.value)
                  + " " + str(o.value))
    # validate cut card
    c = Card(None, None)
    if c.__str__() != 'THE CUT CARD':
        print("failed at cut")
        print(c + " _vs_ " + 'THE CUT CARD')
        valid = False
    return valid


class CardFace(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        if 2 <= self.value <= 9:
            return str(self.value)
        elif self.value == 10:
            return 't'
        elif self.value == 11:
            return 'j'
        elif self.value == 12:
            return 'q'
        elif self.value == 13:
            return 'k'
        else:
            return 'a'


class Suit(Enum):
    SPADES = 0
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3


def make_two_card_hands_tuple():
    hands = ()  # initialise empty tuple
    for i in CardFace:
        for j in CardFace:
            key = "".join(sorted(i.__str__() + j.__str__()))  # had to override toString/ __str__() method to get
            # desired char response.
            if key not in hands:
                hands = hands + (key,)
    # print(f"tuple became {len(hands)} elements long")
    return hands


def make_three_card_hands_tuple():
    hands_set = []
    for i in CardFace:
        for j in CardFace:
            for k in CardFace:
                el = "".join(sorted(i.__str__() + j.__str__() + k.__str__()))
                if el not in hands_set:
                    hands_set.append(el)

    invalid_keys = []
    for el in hands_set:
        # outline initial matrix of card values based on card face enums
        card_vals = [0, 0, 0]
        n = 0
        for i in el:
            if i in ['2', '3', '4', '5', '6', '7', '8', '9']:
                card_vals[n] = int(i)
            elif i in ['t', 'j', 'q', 'k']:
                card_vals[n] = 10
            else:
                card_vals[n] = 11
            n += 1

        # count number of aces present
        num_aces = el.count('a')

        all_aces_converted = False
        if num_aces == 0:
            all_aces_converted = True

        # convert values of aces in bust hands to 1 while hand is bust
        i = 0
        num_aces_converted = 0
        while (not all_aces_converted) and sum(card_vals) > 21:
            if el[i] == 'a':
                card_vals[i] = 1
                num_aces_converted += 1
                if num_aces == num_aces_converted:
                    all_aces_converted = True
            i += 1

        if all_aces_converted and sum(card_vals) > 21:
            # if all aces in hand have been converted and total value still exceeds 21 -> this hand is bust
            invalid_keys.append(el)
    for k in invalid_keys:
        hands_set.remove(k)

    hands_tuple = ()
    for n in hands_set:
        hands_tuple = hands_tuple + (n,)
    return hands_tuple


class Card:
    def __init__(self, suit, face):
        if suit is None and face is None:
            self.cut_card = True
        else:
            self.cut_card = False
            self.suit = suit
            self.face = face
            self.value = Card.determine_card_val(face.value)

    @staticmethod
    def determine_card_val(index):
        if 2 <= index <= 10:
            return index
        elif 11 <= index <= 13:
            return 10
        else:
            return 11  # ace valued at 11 by default. Soft hands can be
            # considered later

    def __str__(self):
        # __str__ dunder method override
        if self.face is not None and self.suit is not None:
            return 'THE ' + str(self.face.name) + ' OF ' + str(self.suit.name)
        else:
            return 'THE CUT CARD'
