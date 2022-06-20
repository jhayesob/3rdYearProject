from Card import Card
from Deck import Deck
from CardCollection import CardCollection


class Shoe(CardCollection):
    # class declaration for shoe
    def __init__(self, depth_pen):
        super().__init__()
        self.depth_pen = depth_pen
        self.construct()

    def construct(self):
        self.cards.clear()
        for x in range(6):
            self.cards.extend(Deck().__getattribute__("cards"))
        self.shuffle()
        # insert cut card at specified depth
        self.cards.insert(self.depth_pen, Card(None, None))

    def take_card(self):
        # build function "getCard" for shoe object to remove the need to think
        # about whether the cut card is encountered and a reshuffle is required

        # checks if the Cut Card has been reached. If it has the shoe is
        # reshuffled before proceeding. The last card in the list is taken.
        return self.cards.pop()
