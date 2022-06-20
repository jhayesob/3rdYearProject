import HiLowPlayer
from Card import CardFace
from Card import Card
import Hand
from ListTree import ListTree
import sys


class BlackjackRound:
    def __init__(self, table):
        self.table = table
        self.round_complete = False
        self.player_wager = 0
        self.players_payout = None
        self.player_insurance_wager = None
        self.player_insurance_outcome = None
        self.player_even_money_wager = None
        self.player_even_money_outcome = None
        self.tc_before_round = None
        self.execution()

    def collect_wagers(self):
        self.player_wager = self.table.player.calculate_wager_amount()
        if type(self.table.player) is HiLowPlayer.HiLowPlayer:
            try:
                self.tc_before_round = self.table.player.get_tc()
            except AttributeError:
                print("method doesnt exist")

    def deal_cards(self):
        self.table.deal_card_to_dealer()
        self.table.deal_card_to_dealer()

        self.table.deal_card_to_player()
        self.table.deal_card_to_player()

        # print(f" player's hand is {[x.face for x in self.table.player.hand.cards]}")
        # print(f" dealer's up-card is {self.table.dealer.hand.cards[0]}")

    def insurance_module(self):
        if self.table.dealer.hand.cards[0].face == CardFace.ACE:
            # print("Insurance bets are about to take place")
            player_has_bj = False

            if self.table.player.hand.check_blackjack():
                player_has_bj = True
                # print("the player's hand is a blackjack")
                if self.table.player.decide_take_even_money():
                    # player paid off 1 to 1 immediately. sacrificing chance to be paid
                    # 3 to 2 if dealer doesn't have blackjack.
                    self.player_even_money_wager = self.player_wager * 2
                    # self.table.player.receive_payout(self.player_wager * 2)
                    # print("Player took even money - winning " + str(self.player_even_money_wager) + " - Round over.")
                    self.table.round_end()
                    self.round_complete = True  # escape
                else:
                    pass
                    # print("player declined even money")
            if self.table.player.decide_take_insurance:
                self.player_insurance_wager = int(self.table.player.post_insurance_bet(self.player_wager))
                # print(f"player posted insurance bet of {self.player_insurance_wager}")
            else:
                pass
                # print("player declined insurance")
                # self.set_players_insurance_bet(key, i.post_insurance_bet(0))
                # --> now treating it as None

            # insurance outcome:
            if self.table.dealer.hand.check_blackjack():
                # print("DEALER HAD BLACKJACK")

                if self.player_insurance_wager:
                    self.player_insurance_outcome = self.player_insurance_wager * 2
                    # self.table.player.receive_payout(self.player_insurance_outcome)

                if not player_has_bj:
                    self.players_payout = -self.player_wager
                    # print("DEALER WON BY BLACKJACK")
                    self.round_complete = True
            else:
                if self.player_insurance_wager:
                    self.player_insurance_outcome = - self.player_insurance_wager

    def the_players_blackjack(self):
        if self.table.player.hand.check_blackjack():
            # print(f'Dealers hand was {[x.face for x in self.table.dealer.hand.cards]}')
            if not self.table.dealer.hand.check_blackjack():
                self.players_payout = int(self.player_wager * 1.5)
                # self.table.player.receive_payout(int(self.player_wager) + self.players_payout)
                # print("Player won by Blackjack - winning " + str(self.players_payout) + " - Round over. ")
                # print(type(self.players_payout))
                self.table.round_end()
            else:
                self.players_payout = 0
                # self.table.player.receive_payout(self.player_wager)
                # print("Round concluded with a 'push'. ")
                self.table.round_end()
            self.round_complete = True

    def player_play_hand(self):
        self.player_take_action(self.table.player.make_choice(self.table.dealer.hand.cards[0]))
        # print("--- Reached end of player's play")

    def player_take_action(self, response, *args):
        # if perfectly wanting to neatly stick to object-oriented approach, could query a "make choice" function in
        # Player class, enact it, then continue to query until the round is complete. Would mean that I need to call
        # this function multiple times, but it would make for logical program design - helping simply coding when
        # integrating more factors into players decisions.

        if len(self.table.player.split_hands.objects) == 0:
            if response == 'std':
                pass
                # print("IMMEDIATE STAND")

            elif response == "h":
                # print("IMMEDIATE HIT")
                self.table.deal_card_to_player()
                if not self.table.player.hand.is_bust():
                    # print(f'Upon hitting, Hand became: {[x.face for x in self.table.player.hand.cards]}')
                    self.player_take_action(
                        self.table.player.make_choice(self.table.dealer.hand.cards[0]))
                else:
                    pass
                    # print("Upon hitting, hand went bust")
                    # print(f'Hand was: {[x.face for x in self.table.player.hand.cards]}')

            elif response == "dd":
                # print("IMMEDIATE DD")
                self.player_wager += self.player_wager
                # print("- updated bet = " + str(self.player_wager))
                self.table.deal_card_to_player()
                if not self.table.player.hand.is_bust():
                    pass
                    # print(f"- player's hand is now: {[x.face for x in self.table.player.hand.cards]}")
                else:
                    pass
                    # print("Upon receiving another card, hand went bust")
                    # print(f'Hand was: {[x.face for x in self.table.player.hand.cards]}')

            elif response == "split":
                # print("IMMEDIATE SPLIT")
                if self.table.player.hand.cards[0].face == CardFace.ACE:
                    h = Hand.Hand(Card(self.table.player.hand.cards[1].suit, CardFace.ACE))
                    # if a pair of aces has been dealt, the hand has been made hard by the second ace value card being
                    # made to value 1. So here a new "ACE" card is being instantiated, so that it is valued at 11.

                    h.set_split_from_aces_true()
                    self.table.player.split_hands.add_children_to_tree([],
                                                                       Hand.Hand(
                                                                           self.table.player.hand.cards[
                                                                               0]), h)
                    self.table.player.split_hands[[0]].set_split_from_aces_true()
                    self.table.player.split_hands[[1]].set_split_from_aces_true()
                else:
                    self.table.player.split_hands.add_children_to_tree([],
                                                                       Hand.Hand(
                                                                           self.table.player.hand.cards[
                                                                               0]),
                                                                       Hand.Hand(
                                                                           self.table.player.hand.cards[
                                                                               1]))
                self.table.deal_card_to_player([0])
                self.table.player.split_hands[[0]].increment_num_splits()
                self.table.deal_card_to_player([1])
                self.table.player.split_hands[[1]].increment_num_splits()

                current_bet = self.player_wager
                self.player_wager = ListTree()
                self.player_wager.add_children_to_tree([], current_bet, current_bet)
                self.player_take_action(
                    self.table.player.make_choice(self.table.dealer.hand.cards[0], [0]), [0])
                # print("Second hand going into recurse...")
                self.player_take_action(
                    self.table.player.make_choice(self.table.dealer.hand.cards[0], [1]), [1])
            else:
                print("failure")
                sys.exit(0)
        else:
            # print(f'Split Hand: {[x.face for x in self.table.player.split_hands[args[0]].cards]} at coordinate: '
            # f'{args[0]}, with {self.table.player.split_hands[args[0]].num_splits} previous splits, and a VALUE '
            # f'OF: {self.table.player.split_hands[args[0]].get_hand_value()} has a response'
            # f' of: ' + response)

            if response == 'std':
                pass
                # print(f'...so player with hand of {[x.face for x in self.table.player.split_hands[args[0]].cards]} is'
                # f' STDing against the dealers: ' + str(self.table.dealer.hand.cards[0]))

            elif response == "h":
                self.table.deal_card_to_player(args[0])
                if not self.table.player.split_hands[args[0]].is_bust():
                    # print(f'...this Hand of: {[x.face for x in self.table.player.split_hands[args[0]].cards]} is'
                    # f' being RECURSIVELY PASSED TO FUNCTION call')
                    self.player_take_action(
                        self.table.player.make_choice(self.table.dealer.hand.cards[
                                                          0], args[0]), args[0])
                else:
                    pass
                    # print(f'..this Hand of: {[x.face for x in self.table.player.split_hands[args[0]].cards]} WENT
                    # BUST')

            elif response == "dd":
                self.player_wager[args[0]] += self.player_wager[args[0]]
                # print("- updated bet = " + str(self.player_wager[args[0]]))
                self.table.deal_card_to_player(args[0])
                if not self.table.player.split_hands[args[0]].is_bust():
                    pass
                    # print(f"- player's hand is now: {[x.face for x in self.table.player.split_hands[args[0]].cards]}")
                else:
                    pass
                    # print(f'..this Hand of: {[x.face for x in self.table.player.split_hands[args[0]].cards]} WENT
                    # BUST')

            elif response == "split":

                current_num_splits = self.table.player.split_hands[args[0]].num_splits
                self.table.player.split_hands.add_children_to_tree(args[0],
                                                                   Hand.Hand(
                                                                       self.table.player.hand.cards[0]),
                                                                   Hand.Hand(
                                                                       self.table.player.hand.cards[1]))
                self.table.deal_card_to_player(args[0] + [0])
                self.table.player.split_hands[args[0] + [0]].set_num_splits(current_num_splits + 1)
                self.table.deal_card_to_player(args[0] + [1])
                self.table.player.split_hands[args[0] + [1]].set_num_splits(current_num_splits + 1)

                current_bet = self.player_wager[args[0]]
                self.player_wager.add_children_to_tree(args[0], current_bet, current_bet)

                self.player_take_action(
                    self.table.player.make_choice(self.table.dealer.hand.cards[0],
                                                  args[0] + [0]), args[0] + [0])
                self.player_take_action(
                    self.table.player.make_choice(self.table.dealer.hand.cards[0],
                                                  args[0] + [1]), args[0] + [1])
            else:
                print("failure")
                sys.exit(0)

    def dealer_play_hand(self):
        # print(f"Dealers hand is: {[x.face for x in self.table.dealer.hand.cards]}, Its value is:"
        # f" {self.table.dealer.hand.get_hand_value()}")
        self.dealer_action(self.table.dealer.make_choice())

    def dealer_action(self, action):
        if action == 'hit':
            self.table.deal_card_to_dealer()
            self.dealer_action(self.table.dealer.make_choice())
            # print(f"After hitting, dealers hand is now: {[x.face for x in self.table.dealer.hand.cards]}. Its value
        # is:" f" {self.table.dealer.hand.get_hand_value()}")
        elif action == 'std':
            pass

    def get_wager_outcome(self, *args):
        # args[0] = hand_index for split hands
        if len(args) == 0:
            if not self.table.player.hand.bust:
                if self.table.dealer.hand.bust:
                    return self.player_wager
                elif (21 - self.table.player.hand.get_hand_value()) < (21 - self.table.dealer.hand.get_hand_value()):
                    # print("closer to 21 than the dealer")
                    return self.player_wager
                elif self.table.player.hand.get_hand_value() == self.table.dealer.hand.get_hand_value():
                    # print("push")
                    return 0
                else:
                    # print("further from 21 than the dealer")
                    return -self.player_wager
            else:
                # print("player bust")
                return -self.player_wager
        else:
            if not self.table.player.split_hands[args[0]].bust:
                if self.table.dealer.hand.bust:
                    return self.player_wager[args[0]]
                elif (21 - self.table.player.split_hands[args[0]].get_hand_value()) < (
                        21 - self.table.dealer.hand.get_hand_value()):
                    return self.player_wager[args[0]]
                elif self.table.player.split_hands[args[0]].get_hand_value() == self.table.dealer.hand.get_hand_value():
                    return 0
                else:
                    return -self.player_wager[args[0]]
            else:
                return -self.player_wager[args[0]]

    def end_game(self):
        if len(self.table.player.split_hands.get_list_tree()) != 0:
            # split hands path
            trie_terminal_indexes = self.table.player.split_hands.get_trie_terminal_indexes()
            wager_outcomes_list = []
            # print(trie_terminal_indexes)
            for i in trie_terminal_indexes:
                wager_outcomes_list.append(self.get_wager_outcome(i))
            # print(f'wager outcomes: {wager_outcomes_list}')
            self.players_payout = ListTree(trie_terminal_indexes, wager_outcomes_list)

            # for i in trie_terminal_indexes:
            # print(f'{self.players_payout[i]} at index: {i}')
            # self.table.player.receive_payout(int(self.player_wager[i]) + self.players_payout[i])

            # now self.playersWagersOutcome holds a trie of the correct structure. The data im passing to it actually
            # shouldn't be hands though. It should be wager outcome ints.

            # right now I want to put the wager outcomes into the list tree. So I need to be passing that into the list
            # tree construction. the hand objects are available freely to address by index from split_hands tree.
        else:
            # non-split hands path
            self.players_payout = self.get_wager_outcome()
            # print(f"wager outcome for round: {self.players_payout}")
        self.table.round_end()

    def execution(self):
        while not self.round_complete:
            self.collect_wagers()
            self.deal_cards()
            self.insurance_module()
            if self.round_complete:
                break
            self.the_players_blackjack()
            if self.round_complete:
                break
            self.player_play_hand()
            self.dealer_play_hand()
            self.end_game()
            if not self.round_complete:
                self.round_complete = True
        self.table.round_end()
