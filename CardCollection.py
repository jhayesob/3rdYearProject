from random import shuffle


class CardCollection:
    def __init__(self):
        self.cards = []

    def __str__(self):
        return_str = ", ".join(str(x) for x in self.cards)
        return return_str
        # __str__ dunder method override

    def shuffle(self):
        shuffle(self.cards)
