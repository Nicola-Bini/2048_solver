import pygame
import time
from game import Game2048
import numpy as np
from montecarlo_algorithm import montecarlo_2048, montecarlo_2048_plot_distribution
from game_gui import Game2048Gui

def __main__(player="human", time_sleep=0):
    '''
            Start game with GUI
            player types ["human", "montecarlo", "keras"]
    '''

    # Initialize game
    game = Game2048()
    game_gui = Game2048Gui(window_size = 1)

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

                    if (score % 1000) != 0:

                        montecarlo_averages = montecarlo_2048(game=game,
                                                             simulations_per_move=24,
                                                             steps=16,
                                                             count_zeros=False)

                    else:


                        montecarlo_2048_plot_distribution(game,
                                                          simulations_per_move= [25, 25, 25],
                                                          steps_per_simulation = [10])

                        montecarlo_averages = montecarlo_2048(game=game,
                                                              simulations_per_move=25,
                                                              steps=16,
                                                              count_zeros=False)

                    # Take montecarlo's suggestion
                    montecarlo_move = np.argmax(montecarlo_averages) + 1

                    # Play the suggested move
                    game.make_move(montecarlo_move)

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

__main__(player="montecarlo")