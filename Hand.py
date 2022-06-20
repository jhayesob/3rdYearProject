from CardCollection import CardCollection
import Card


class Hand(CardCollection):
    def __init__(self, *card_args):
        super().__init__()  # class initialisation based on super class
        self.splitFromAces = False
        self.num_splits = 0
        # gotta note that if a hand resulting from a split pair of aces receives
        # another ace: one ace is valued at 11 and the other is valued at 1.
        # self.value = None
        self.soft = False
        self.bust = False
        # attributes soft and hand update when addToHand() is used.
        # is pair is only called individually outside this class.

        # constructor allows programmer to pass a variable number of existing
        # cards into the instantiation of a new hand. Useful for split hands.
        for x in card_args:
            self.add_to_hand(x)
            if x.value == 11:
                self.soft = True

    def set_split_from_aces_true(self):
        self.splitFromAces = True

    def increment_num_splits(self):
        self.num_splits += 1

    def set_num_splits(self, n):
        self.num_splits = n

    def is_pair(self):
        # class method checks if a hand of two cards is a pair.
        cards = self.cards
        if len(cards) == 2:
            if cards[0].face == cards[1].face:
                return True
            else:
                return False
        else:
            return False

    def is_soft(self):
        card_vals = []
        for i in range(len(self.cards)):
            if self.cards[i].face.__str__() in ['2', '3', '4', '5', '6', '7', '8', '9']:
                card_vals.append(int(self.cards[i].face.__str__()))
            elif self.cards[i].face.__str__() in ['t', 'j', 'q', 'k']:
                card_vals.append(10)
            else:
                card_vals.append(11)
        num_aces = card_vals.count(11)
        num_aces_converted = 0
        all_aces_converted = False
        if num_aces == 0:
            all_aces_converted = True
        i = 0
        while (not all_aces_converted) and sum(card_vals) > 21:
            if card_vals[i] == 11:
                card_vals[i] = 1
                num_aces_converted += 1
                if num_aces == num_aces_converted:
                    all_aces_converted = True
            i += 1
        if card_vals.count(11):
            return True
        else:
            return False

    def add_to_hand(self, card):
        self.cards.append(card)
        if card.value == 11 and not self.soft and not self.contains_aces_made_hard():
            self.soft = True
        if self.is_bust():
            self.bust = True
        elif self.check_needs_hard():
            # print("Hand is getting made hard")
            self.make_hard()

    def contains_aces_made_hard(self):
        for c in self.cards:
            if c.face == Card.CardFace.ACE and c.value == 1:
                return True
        return False

    def is_bust(self):
        return self.get_hand_value() > 21 and not self.check_needs_hard()

    def check_needs_hard(self):
        if self.get_hand_value() > 21 and any([card.value == 11 for card in self.cards]):
            return True

    def make_hard(self):
        if self.is_pair():
            seen_first_ace = False
            for card in self.cards:
                if card.value == 11 and not seen_first_ace:
                    seen_first_ace = True
                elif card.value == 11 and seen_first_ace:
                    card.value = 1
                    self.soft = False
        else:
            ace_converted = False
            for card in self.cards:
                if card.value == 11 and not ace_converted:
                    card.value = 1
                    self.soft = False
                    ace_converted = True
            if not ace_converted:
                print("no ace here.")

    def check_blackjack(self):
        # only two-card hands make blackjacks
        if len(self.cards) == 2 and self.soft:
            for i in self.cards:
                if i.value == 10:
                    return True
        return False

    def get_hand_value(self):
        val = 0
        for k in self.cards:
            val += k.value
        return val

    @staticmethod
    def test_check_blackjack_module():
        card_list = []
        hand_list = []
        for i in Card.CardFace:
            card_list.append(Card.Card(Card.Suit.DIAMONDS, i))
        for i in card_list:
            for o in card_list:
                if (i.value > 9 and o.value > 9) and i.face != o.face:
                    h = Hand()
                    h.add_to_hand(i)
                    h.add_to_hand(o)
                    hand_list.append(h)
        for i in hand_list:
            # print(f' Hand is {[x.face for x in i.cards]} and Soft is: ' + str(i.soft)) - okay soft is accurate
            print(f' Hand is {[x.face for x in i.cards]} and BlackJack is: ' + str(i.check_blackjack()))
