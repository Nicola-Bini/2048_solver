import random
from game import Game2048
import numpy as np
from copy import deepcopy
import time
import matplotlib.pyplot as plt

def Montecarlo2048(game, simulations_per_move, steps, count_zeros=False, print_averages=True):
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

        average_scores[(move-1)] = np.average(score_list)

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

    return average_scores