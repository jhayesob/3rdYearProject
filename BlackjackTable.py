from Dealer import Dealer
from Shoe import Shoe
from TrueCountAdjustedShoe import TrueCountAdjustedShoe
from Hand import Hand
from ListTree import ListTree


class BlackjackTable:
    def __init__(self, *sim_args):
        self.dealer = Dealer()  # dealer holds all data on house - eg: shoe
        # here can investigate into the keys provided in kwargs and use the right shoe
        # if depth_pen is provided then pss that into normal shoe

        # kwargs isnt working so just gonna go with args.
        # args[0] = depth_pen
        # args[1] = true_count
        if sim_args[0] != -10 and sim_args[1] == -10:
            self.shoe = Shoe(sim_args[0])
        elif sim_args[1] != -10 and sim_args[0] == -10:
            # alternate shoe construction
            self.shoe = TrueCountAdjustedShoe(sim_args[1])
            # if true_count is provided then pass that into altered_shoe
        self.player = None

    def player_joins_table(self, player):
        self.player = player

    def reshuffle_shoe(self):
        self.player.notify_shuffle()
        self.shoe.construct()

    def deal_card_to_player(self, *args):
        c = self.shoe.take_card()
        if c.cut_card is True:
            self.reshuffle_shoe()
            g = self.shoe.take_card()
            self.player.notify_card(g)
            if args:
                self.player.split_hands[args[0]].add_to_hand(g)
            else:
                self.player.hand.add_to_hand(g)
        else:
            self.player.notify_card(c)
            if args:
                self.player.split_hands[args[0]].add_to_hand(c)
            else:
                self.player.hand.add_to_hand(c)

    def deal_card_to_dealer(self):
        c = self.shoe.take_card()
        if c.cut_card is True:
            self.reshuffle_shoe()
            g = self.shoe.take_card()
            self.player.notify_card(g)
            self.dealer.hand.add_to_hand(g)
        else:
            self.player.notify_card(c)
            self.dealer.hand.add_to_hand(c)

    def round_end(self):
        self.dealer.hand = Hand()
        self.player.hand = Hand()
        self.player.split_hands = ListTree()
