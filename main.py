import pygame
import time
from game import Game2048
import numpy as np
from montecarlo_algorithm import montecarlo_2048, montecarlo_2048_plot_distribution
from game_gui import Game2048Gui
import os
import pandas as pd


def convert_str_matrix_to_numpy(grid):
    grid = grid.replace("\n", ",")
    arr_lst = []
    lst = ""

    for char in grid:
        lst = lst + char
        if char == ",":
            lst = lst.strip(" [],")
            print(lst)
            lst = lst.split()
            lst = list(map(int, lst))
            arr_lst.append(lst)
            lst = ""

    lst = lst.strip(" [],")
    print(lst)
    lst = lst.split()
    lst = list(map(int, lst))
    arr_lst.append(lst)

    return np.array(arr_lst, dtype="object")


def __main__(player="human", time_sleep=0, save_replay=False, replay_name=""):
    '''
            Start game with GUI
            player types ["human", "montecarlo", "keras"]
    '''


    # Initialize game
    game = Game2048()
    game_gui = Game2048Gui(window_size = 1)

    if player == "watch_replay":

        # check if replay exists
        if os.path.isfile("./replays/" + replay_name + ".csv"):
            print(f"Starting replay: {replay_name} \n")
        else:
            print(f"Error replay {replay_name} does not exist\n")
            quit()

        df_game_states = pd.read_csv("./replays/" + replay_name + ".csv")
        print(df_game_states.dtypes)
        game.game_grid = convert_str_matrix_to_numpy(df_game_states.loc[0, 'game_state'])


        for i in range(len(df_game_states)-1):
            time.sleep(0.1)
            print(df_game_states.loc[i+1, 'game_state'])
            game.game_grid = convert_str_matrix_to_numpy(df_game_states.loc[i+1, 'game_state'])
            print(game.game_grid)
            game_gui.draw_game(game)

        if len(game.check_allowed_moves()) == 0:
            game_gui.draw_game(game, game_over=True)

        input("Replay finished, press enter to quit")
        quit()


    # Create replay file
    if save_replay:
        name_not_valid = True
        while name_not_valid:
            replay_name = input("How do you want to call this replay?")

            # Check if there is a replay with this name
            if os.path.isfile("./replays/" + replay_name + ".csv"):
                print(f"the name {replay_name} is taken, choose another name \n")
            else:
                name_not_valid = False

        # Save current game
        print(f"Creating new replay with name '{replay_name}'")
        game.save_game(replay_name, "n/d")

    while game._running:

        game_gui.draw_game(game)

        # Check if it's game over
        if len(game.check_allowed_moves()) > 0:

            if player == "human":
                key = game_gui.wait_for_key()

                if key == 'q':
                    game._running = False

                if key != 'nothing':
                    game.make_move(key)

            elif player == "montecarlo":

                # Sleep between moves
                if time_sleep > 0:
                    time.sleep(time_sleep)

                if len(game.check_allowed_moves()) > 0:

                    # Montecarlo's suggested move
                    score = game.calculate_score(score_type="simple_sum")
                    if score < 1000:

                        montecarlo_averages = montecarlo_2048(game=game,
                                                             simulations_per_move=25,
                                                             steps=6,
                                                             count_zeros=False)


                    else:

                        montecarlo_averages = montecarlo_2048(game=game,
                                                              simulations_per_move=1024,
                                                              steps=16,
                                                              count_zeros=False)


                    # Take montecarlo's suggestion
                    montecarlo_move = np.argmax(montecarlo_averages) + 1

                    # Play the suggested move
                    game.make_move(montecarlo_move)

                    if save_replay:
                        game.save_game(replay_name, montecarlo_move)

                # Game over
                # else:
                #     print("LOST")
                #     if save_best_score == True:
                #         print("saving score..")
                #
                #         # Get record score
                #         scoreboard = pd.read_csv("scoreboard.csv", index_col=False)
                #
                #         # Get current score
                #         score = game.calculate_score(classic_score=True)
                #
                #         # Get current generation
                #         generation = scoreboard["generation"].max() + 1
                #
                #         # Add current score to the scoreboard
                #         current_data = {"generation": generation,
                #                         "score": score}
                #
                #         scoreboard = scoreboard.append(current_data, ignore_index=True)
                #         scoreboard.to_csv("scoreboard.csv", index_label=False, index=False)
                #
                #         _running = False


        else:
            game_gui.draw_game(game, game_over=True)
            key = game_gui.wait_for_key()
            while key != 'q':
                key = game_gui.wait_for_key()
            game._running = False


        # Update game


    return

__main__(player="montecarlo", save_replay=True, replay_name="test1")