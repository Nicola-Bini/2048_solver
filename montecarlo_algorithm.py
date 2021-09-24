import random
from game import Game2048
import numpy as np
from copy import deepcopy
import time
import matplotlib.pyplot as plt

def montecarlo_2048(game, simulations_per_move, steps, count_zeros=False, print_averages=True, return_scores=False):
    """
    Test each possible move, run montecarlo simulations and return a dictionary of average scores,
    one score for each possible move
    """

    # Retrieve game score at the current state
    game_score = game.calculate_score()

    # Retrieve list of possible moves
    allowed_moves = game.check_allowed_moves()

    # Create a dictionary to store average scores per allowable move
    average_scores = np.zeros(4)

    # Will contain 4 lists of scores, one list for each starting move (LEFT, DOWN, RIGHT, UP)
    scores_per_move = [[0]] * 4

    for move in allowed_moves:

        score_list = []

        for simulation in range(simulations_per_move):

            # Create a a copy of the game at the current state
            game_copy = deepcopy(game)

            game_copy.make_move(move)

            for i in range(steps):

                # Check if there is any move allowed
                if len(game_copy.check_allowed_moves()) > 0:

                    # Pick a random move within the allowed ones
                    random_move = random.choice(game_copy.check_allowed_moves())
                    game_copy.make_move(random_move)

            # append simulation result
            if count_zeros == True:
                score_list.append(game_copy.calculate_score(score_type="simple_sum"))
            else:
                score_list.append(game_copy.calculate_score(score_type="simple_sum"))

        scores_per_move[move-1] = score_list
        average_scores[move-1] = np.average(score_list)

    if print_averages:
        print("[1] LEFT score: ",  average_scores[0])
        print("[2] DOWN score: ",  average_scores[1])
        print("[3] RIGHT score: ", average_scores[2])
        print("[4] UP score: ",    average_scores[3])

        print("average_scores: ", average_scores)
        choice = np.argmax(average_scores) + 1

    steal = 0
    for value in average_scores:
        if value > 0:
            steal = 1

    if steal == 0:
        random_scores = np.zeros(4)
        random_scores[np.random.choice([0,1,2,3])] = 1
        return random_scores

    if return_scores:
        return scores_per_move
    else:
        return average_scores



def montecarlo_2048_plot_distribution(game, simulations_per_move, steps_per_simulation):
    """
    Test each possible move, run montecarlo simulations and return a dictionary of average scores,
    one score for each possible move
    """

    results = []

    # moves in specific order
    moves = ["left", "down", "right", 'up']
    for n_simulations in simulations_per_move:
        for steps in steps_per_simulation:
            montecarlo_scores = montecarlo_2048(game, n_simulations, steps, return_scores=True)
            print(montecarlo_scores)
            results.append({"n_simulations" : n_simulations,
                           "steps"                : steps,
                           "scores"               : {}})

            for i, move in enumerate(moves):
                results[-1]["scores"].setdefault(move, montecarlo_scores[i])

    fig, axs = plt.subplots(len(results), 4)
    for i, result in enumerate(results):
        for j, move in enumerate(moves):

            if ((max(result["scores"][move]) - min(result["scores"][move]))/2) % 1 == 0:
                n_bins = int((max(result["scores"][move]) - min(result["scores"][move])))
                print(n_bins)
            else:
                n_bins = int((max(result["scores"][move]) - min(result["scores"][move]))) + 1
                print(n_bins)
            if n_bins == 0:
                n_bins = 1
            axs[i, j].hist(result["scores"][move], bins = n_bins)
            axs[i, j].set_title(f'move:{move}, n_simulations: {result["n_simulations"]}, steps: {result["steps"]}')
            axs[i, j].axvline(np.mean(result["scores"][move]), color="red")
    fig.show()
    plt.close(fig)