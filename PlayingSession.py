from BlackjackTable import BlackjackTable
from MimicTheDealerPlayer import MimicTheDealerPlayer
from NeverBustPlayer import NeverBustPlayer
from BasicStrategyPlayer import BasicStrategyPlayer
from HiLowPlayer import HiLowPlayer, HiLowDeviationsPlayer
from WongHalvesPlayer import WongHalvesPlayer, WongHalvesDeviationsPlayer
from AceFivePlayer import AceFivePlayer
from KOPlayer import KOPlayer
from BlackjackRound import BlackjackRound
import ListTree


class PlayingSession:
    def __init__(self, num_rounds, player_type, *sim_args):
        # args to define different depth_pen \ true_count \ bet spread simulation specifications
        self.num_rounds = num_rounds
        self.player_type = player_type
        self.sim_args = sim_args

        self.initial_units_bet = []
        self.round_bets_totals = []  # cumulative
        self.round_bets_outcomes = []
        self.tc_before_rounds = []
        self.betting_adv_val = 0  # float value for the house advantage seen from the betting outcomes of these rounds
        self.do()

    def do(self):
        casino_table = BlackjackTable(self.sim_args[0], self.sim_args[1])
        if self.player_type == 'basic_strategy_player':
            casino_table.player_joins_table(BasicStrategyPlayer())
        elif self.player_type == 'mimic_the_dealer_player':
            casino_table.player_joins_table(MimicTheDealerPlayer())
        elif self.player_type == 'never_bust_player':
            casino_table.player_joins_table(NeverBustPlayer())

        elif self.player_type == 'hi_low_player':
            casino_table.player_joins_table(HiLowPlayer(self.sim_args[2]))
        elif self.player_type == 'wong_halves_player':
            casino_table.player_joins_table(WongHalvesPlayer(self.sim_args[2]))
        elif self.player_type == 'ace_five_player':
            casino_table.player_joins_table(AceFivePlayer(self.sim_args[2]))

        elif self.player_type == 'hi_low_deviations_player':
            casino_table.player_joins_table(HiLowDeviationsPlayer(self.sim_args[2]))
        elif self.player_type == 'wong_halves_deviations_player':
            casino_table.player_joins_table(WongHalvesDeviationsPlayer(self.sim_args[2]))
        elif self.player_type == 'knock_out_player':
            casino_table.player_joins_table(KOPlayer())
        else:
            print('cant tell what player type should be used to run these rounds: likely problem with input string for '
                  'player type')

        for it in range(self.num_rounds):
            r = BlackjackRound(casino_table)
            # no need to store the r object in the greater scope of the program, so im choosing to neglect it with
            # the aim of decreasing to length of time it takes to run simulations and retrieve results.

            if self.player_type == 'hi_low_player':
                self.tc_before_rounds.append(r.tc_before_round)

            # counting up bets/returns values
            bets_this_round = 0
            bet_outcomes_this_round = 0
            if r.player_insurance_wager:
                bets_this_round += r.player_insurance_wager
                bet_outcomes_this_round += r.player_insurance_outcome
            if type(r.player_wager) is ListTree.ListTree:
                indexes = r.player_wager.get_trie_terminal_indexes()
                for i in indexes:
                    bets_this_round += r.player_wager[i]
                    bet_outcomes_this_round += r.players_payout[i]
            else:
                bets_this_round += r.player_wager
                bet_outcomes_this_round += r.players_payout
            if it == 0:
                self.round_bets_totals.append(bets_this_round)
                self.round_bets_outcomes.append(bet_outcomes_this_round)
            else:
                self.round_bets_totals.append(bets_this_round + self.round_bets_totals[-1])
                self.round_bets_outcomes.append(bet_outcomes_this_round + self.round_bets_outcomes[-1])
                # Cumulate bets and betting returns over all rounds
        self.betting_adv_val = self.round_bets_outcomes[-1] / self.round_bets_totals[-1] * 100
