import Card
from CardCollection import CardCollection


def valid_shuffle_test():
    d = Deck()
    print(d)  # no need for an outputDeckToConsole() function with the __str__()
    # override
    d.shuffle()
    print(d)
    # options were to either to make function from method or to make method static
    # lil consolidation:
    # pieces of code called by name where data is *explicitly* passed are more
    # appropriate to be called functions
    #   explicitly?... means the variable/data is passed whereas implicitly means
    #   you're passing an obj
    # code that operates on data that is implicitly passed is more appropriate for
    # use in a method
    #
    # deckTest1() doesn't need to be passed an object to operate on... so I decide
    # to declare it as a function from method


def valid_instant_test(deck):
    seen_cards = []
    for i in deck.cards:
        if i not in seen_cards:
            seen_cards.append(i)
        else:
            return False
    if len(seen_cards) != 52:
        return False
    else:
        return True


class Deck(CardCollection):
    def __init__(self):
        super().__init__()
        self.build_deck()
        # self.shuffle()

    def build_deck(self):
        # Hash Maps vs Nested Loops
        # maps will be faster but takes memory to allocate the lists data into
        # a map. nested loop is suitable here tho because we do need to iterate
        # over every single combination and list length is limited.
        for x in Card.Suit:
            for y in Card.CardFace:
                self.cards.append(Card.Card(x, y))
