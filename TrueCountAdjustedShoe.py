from Card import Card, CardFace, Suit
from CardCollection import CardCollection
import random
from math import floor, ceil


def TrueCountShoeTestHarness():
    print(ceil(4.5))
    print(ceil(-4.5))
    print(floor(4.5))
    print(floor(-4.5))
    for t_c in range(-6, 7):
        low_cards_num = 0
        mid_cards_num = 36
        high_cards_num = 0
        if t_c == 0:
            low_cards_num = 60
            high_cards_num = 60
        else:
            r_c = t_c * 3
            if r_c > 0:
                high_cards_num = 60 + ceil(r_c / 2)
                low_cards_num = 60 - (r_c - (high_cards_num - 60))
            else:
                low_cards_num = 60 - floor(r_c / 2)  # r_c is negative, so double negation will cause addition
                high_cards_num = 60 - (-r_c - (low_cards_num - 60))
        print(f"t_c: {t_c} | r_c: {r_c}| low_cards_num = {low_cards_num} | high_cards_num = {high_cards_num}")


class TrueCountAdjustedShoe(CardCollection):
    # class declaration for shoe
    def __init__(self, specified_true_count):
        super().__init__()
        self.t_c = specified_true_count
        self.construct()

    def construct(self):
        # place cards in list
        # shoe should be 3*52 = 156 cards long |
        # 156 / 13 = 12
        if self.t_c == 0:
            for i in range(60):
                # generate low cards
                self.cards.append(Card(Suit.CLUBS, random.choice([CardFace.TWO, CardFace.THREE, CardFace.FOUR,
                                                                  CardFace.FIVE, CardFace.SIX])))
            for i in range(36):
                # generate mid-value cards
                self.cards.append(
                    Card(Suit.CLUBS, random.choice([CardFace.SEVEN, CardFace.EIGHT, CardFace.NINE])))
            for i in range(60):
                # generate high cards
                self.cards.append(Card(Suit.CLUBS, random.choice([CardFace.TEN, CardFace.JACK, CardFace.QUEEN,
                                                                  CardFace.KING, CardFace.ACE])))
        else:
            r_c = self.t_c * 3
            low_cards_num = 0
            mid_cards_num = 36
            high_cards_num = 0
            if r_c > 0:
                high_cards_num = 60 + ceil(r_c / 2)
                low_cards_num = 60 - (r_c - (high_cards_num - 60))
            else:
                low_cards_num = 60 - floor(r_c / 2)  # r_c is negative, so double negation will cause addition
                high_cards_num = 60 - (-r_c - (low_cards_num - 60))

            for i in range(low_cards_num):
                # generate low cards
                self.cards.append(Card(Suit.CLUBS, random.choice([CardFace.TWO, CardFace.THREE, CardFace.FOUR,
                                                                  CardFace.FIVE, CardFace.SIX])))
            for i in range(mid_cards_num):
                # generate mid-value cards
                self.cards.append(Card(Suit.CLUBS, random.choice([CardFace.SEVEN, CardFace.EIGHT, CardFace.NINE])))
            for i in range(high_cards_num):
                # generate high cards
                self.cards.append(Card(Suit.CLUBS, random.choice([CardFace.TEN, CardFace.JACK, CardFace.QUEEN,
                                                                  CardFace.KING, CardFace.ACE])))
        self.shuffle()
        self.cards.insert(0, Card(None, None))
        # insert cut card at position 0

    def take_card(self):
        return self.cards.pop()
