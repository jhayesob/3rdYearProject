from time import time, strftime
from PlayingSession import PlayingSession
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import pandas as pd
plt.style.use('seaborn')


# Program designed and developed by James O'Brien as part of Final Year Project: "Investigation And Simulation Of Card
# Counting Methods In Blackjack" - Computer Science B.Sc. - University Of East Anglia.

# Personal/Student Email: jhayesobrien@gmail.com / j.obrien2@uea.ac.uk
# time of program creation: September 2021
# date of final edit: June 2022


def get_last_round_val(e):
    return e.betting_adv_val


def simulation(plot_type):
    # 'plot_betting_returns' || 'plot_betting_advantage'

    start_time = time()

    num_sessions = 20000
    num_rounds = 200
    x_axis_plots = [n for n in range(1, num_rounds + 1)]
    set_depth_pen = -78

    labels = []
    y_finals = []

    # To simulate card counting methods using different betting spreads
    # '1_to_8_bet_spread' || '1_to_12_bet_spread'
    for balanced_count_bet_spread in ['1_to_8_bet_spread', '1_to_12_bet_spread']:

        # 'mimic_the_dealer_player' || 'never_bust_player' || 'basic_strategy_player'
        # 'hi_low_player' || 'wong_halves_player' || 'ace_five_player' || 'knock_out_player'
        # 'hi_low_deviations_player' || 'wong_halves_deviations_player'

        #
        # ['mimic_the_dealer_player', 'never_bust_player', 'basic_strategy_player']
        for playing_style in ['hi_low_player', 'wong_halves_player', 'ace_five_player']:
            playing_sessions_list = []
            total_bets_made = 0
            total_bets_outcomes = 0  # integer variables tracking total value bet/won over rounds

            for it in range(num_sessions):
                # playing sessions executed
                playing_session = PlayingSession(num_rounds, playing_style, set_depth_pen, -10,
                                                 balanced_count_bet_spread)
                # args[0] = depth_pen | args[1] = true_count | args[2] = balanced count players bet spread

                # track betting values over all rounds simulated
                total_bets_made += playing_session.round_bets_totals[-1]
                total_bets_outcomes += playing_session.round_bets_outcomes[-1]
                playing_sessions_list.append(playing_session)

            # Graph plot of median round outcome for playing strategy

            playing_sessions_list.sort(key=get_last_round_val)  # sort playing sessions in order of betting performance

            lower_bound_index = round((len(playing_sessions_list) / 20) * 9)
            upper_bound_index = round((len(playing_sessions_list) / 20) * 11)
            bets_in_bounds = 0
            returns_in_bounds = 0
            for s in range(lower_bound_index, upper_bound_index):
                bets_in_bounds += playing_sessions_list[s].round_bets_totals[-1]
                returns_in_bounds += playing_sessions_list[s].round_bets_outcomes[-1]

            y_axis_plots = []
            # graphing the betting results over the rounds.
            for r_num in range(num_rounds):
                round_bets = 0
                round_returns = 0
                count = 0
                for s in range(lower_bound_index, upper_bound_index):
                    round_bets += playing_sessions_list[s].round_bets_totals[r_num]
                    round_returns += playing_sessions_list[s].round_bets_outcomes[r_num]
                    count += 1

                # Selection statement for graph output # 'plot_betting_returns' || 'plot_betting_advantage'
                if plot_type == 'plot_betting_returns':
                    y_axis_plots.append(round_returns / count)
                elif plot_type == 'plot_betting_advantage':
                    ratio_of_bets_vs_returns = (round_returns / round_bets) * 100
                    y_axis_plots.append(ratio_of_bets_vs_returns)
            # 'hi_low_player' || 'wong_halves_player' || 'ace_five_player' || 'knock_out_player'
            # 'hi_low_deviations_player' || 'wong_halves_deviations_player'
            if playing_style in ['hi_low_player', 'wong_halves_player', 'ace_five_player', 'hi_low_deviations_player',
                                 'wong_halves_deviations_player']:
                label = f"{playing_style} {balanced_count_bet_spread}"
            else:
                label = f"{playing_style}"
            labels.append(label)
            y_finals.append(y_axis_plots[-1])
            plt.plot(x_axis_plots, y_axis_plots, linewidth=1, label=label)

            with open('end.txt', 'a') as file:
                file.write(f"\nLocal time: " + strftime("%a, %d %b %Y %I:%M:%S %p %Z") +
                           f"\nOver {num_sessions} sessions, an average of the 10% median performing sessions was taken"
                           f"\n{num_rounds} Hands were played following: {label} "
                           f"\nBets made here = {bets_in_bounds} | Total returns made = {returns_in_bounds}. "
                           f"\n-> Hence, house adv over this subsection = {(returns_in_bounds / bets_in_bounds) * 100}"
                           f"\nHouse adv over all rounds simulated = {(total_bets_outcomes / total_bets_made) * 100}%"
                           f"\n| Shoe Depth penetration was {set_depth_pen} | \n")
    end_time = time()
    with open('end.txt', 'a') as file:
        file.write(f"Program duration was: {end_time - start_time}. \n")

    plt.ylim([min(y_finals) - (6 * (max(y_finals) - min(y_finals))),
              max(y_finals) + (6 * (max(y_finals) - min(y_finals)))])
    # for plot of results for balanced counts across the 2 different bet spreads, the max deviation between final values
    # should be around 0.4, so 6 is a good multiplier in the final axis scale.

    # for results plot of basic strategy vs mimic the dealer + nobust -> this equation won't produce suitable y limits.
    # comment out this line and paste in "plt.ylim(-10, 5)" instead

    plt.grid(True)
    plt.title("Winnings/Losses By Round For Average Of Median 10% Performing Playing Sessions")
    plt.xlabel("Rounds")
    plt.ylabel("Betting Outcomes (£)")
    plt.legend(labels)
    plt.show()


def graph_frequency_of_tcs():
    start_time = time()

    num_sessions = 10000
    num_rounds = 200
    playing_style = 'hi_low_player'
    set_depth_pen = -78

    count_instances = {}
    for it in range(num_sessions):
        playing_session = PlayingSession(num_rounds, playing_style, set_depth_pen, -10)  # playing sessions executed
        for c in playing_session.tc_before_rounds:
            if c in count_instances.keys():
                # add to the c_index_frequency at that index
                count_instances[c] += 1
            else:
                count_instances[c] = 1

    tc_vals = []
    for k in count_instances.keys():
        for i in range(count_instances[k]):
            tc_vals.append(k)

    #
    # Form gaussian distribution
    #  -->  gaussian distribution didn't really match the exact shape needed for this plot. It was the closest graph
    #       plot that I could learn how to use to visually replicate the function, but it was wrong .
    #       Ultimately, excel line plot diagram was used in the report instead.

    # numpy array of x points for line graph plot
    x = np.arange(-3, 3, 0.1)
    y = norm.pdf(x, 0, (np.std(tc_vals)))  # -> altered standard deviation value because this form of
    # didn't actually properly represent the data.
    print(dict(sorted(count_instances.items())))
    counts = []
    num_instances = []
    c_percentages = []
    for k in sorted(count_instances.keys()):
        counts.append(k)
        num_instances.append(count_instances[k])
        c_percentages.append((count_instances[k] / (num_rounds * num_sessions)) * 100)

    # represent data in data frame
    simulation_data = {'True Count': counts, 'Number Of Instances': num_instances, '% Of Instances': c_percentages}
    df = pd.DataFrame(simulation_data)
    print(df)

    # new data frame for percentage of instances where tc >= 1...
    print(f"percentage of instances where tc >= 1: {sum(c_percentages[counts.index(1):])}")

    # poor graph plot representation unused
    plt.plot(x, y, linewidth=1)
    plt.legend(["Extrapolated Curve From True Count Data"])
    plt.grid(True)
    plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
    plt.title(f"Gaussian Distribution For Frequency Of True Counts Across {num_sessions * num_rounds} Rounds")
    plt.xlabel("True Count")
    plt.ylabel("% Of All Instances For Each True Count")

    end_time = time()
    print(f"Program duration was: {end_time - start_time}. \n")
    plt.show()

    # def func(x, mean, std):
    # return (1 / (std * np.sqrt(2 * np.pi))) * np.exp((-1 / 2) * ((x - mean) / std) ** 2)


def graph_ev_across_true_count():
    start_time = time()
    num_sessions = 20000
    num_rounds = 200
    playing_style = 'basic_strategy_player'
    rows = []
    # store how much bet / how much returned / house adv in dataframe
    # bar graph instead??
    columns = [n for n in range(-3, 5)]

    bets_over_tcs = []
    returns_over_tcs = []

    for tc in range(-3, 5):
        total_bets_made = 0
        total_bets_outcomes = 0
        for it in range(num_sessions):
            playing_session = PlayingSession(num_rounds, playing_style, -10, tc)
            # num_rounds | player_type | args[0] = depth_pen | args[1] = true_count
            for r in range(num_rounds):
                total_bets_made += playing_session.round_bets_totals[r]
                total_bets_outcomes += playing_session.round_bets_outcomes[r]

        # store house advantage values across different set true counts
        bets_over_tcs.append(total_bets_made)
        returns_over_tcs.append(total_bets_outcomes)
        rows.append((total_bets_outcomes / total_bets_made) * 100)
    house_adv_across_rounds = []
    for i in range(len(columns)):
        r = round(((returns_over_tcs[i] / bets_over_tcs[i]) * 100), 2)
        house_adv_across_rounds.append(r)

    simulation_data = {'True Count': columns, 'Bets Made': bets_over_tcs, 'Returns': returns_over_tcs,
                       'House Adv Present': house_adv_across_rounds}
    df = pd.DataFrame(simulation_data)
    print(df)

    plt.title("Change of % House Advantage Value as Shoe True Counts Differ")
    plt.xlabel("True Count of Shoe")
    plt.ylabel("House Advantage % Value Across Simulated Rounds")

    plt.bar(columns, rows, width=0.3, edgecolor='black')
    plt.plot(columns, rows, linewidth=0.8, color='black', label='trend of HouseAdv vs True Count')

    plt.grid(True)
    end_time = time()
    print(f" Program duration was: {end_time - start_time}")
    plt.show()


if __name__ == '__main__':
    # PlotType Arguments List:    'plot_betting_returns' || 'plot_betting_advantage'
    simulation('plot_betting_advantage')
    # graph_frequency_of_tcs()
    # graph_ev_across_true_count()
    # BasicStrategyPlayer.basic_strategy_test_harness()
    # TrueCountAdjustedShoe.TrueCountShoeTestHarness()
