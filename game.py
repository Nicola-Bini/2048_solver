import numpy as np
import random
import pygame
import time
from pygame.locals import *
import os
import pandas as pd

class Game2048():

    def __init__(self):
        self.game_grid = np.zeros((4, 4), dtype='int')

        self.insert_new_number(new_game=True)
        self.insert_new_number(new_game=True)
        self._running = True
        self.total_moves = 0


    def insert_new_number(self, new_game=False):

        '''
        Insert a new number in a random location of the current instance of the game.
        Insert a 2 with a 0.9 probability, and 4 with 0.1 probability.

        :param new_game: The game starts with the number "2" in 2 cells
        '''

        if new_game == True:
            new_number = 2
        else:
            new_number = np.random.choice([2, 4], p=[0.9, 0.1])

        pos1 = random.randint(0, 3)
        pos2 = random.randint(0, 3)


        # Keep looking for a grid position until it finds one
        while self.game_grid[pos1, pos2] != 0:
            pos1 = random.randint(0, 3)
            pos2 = random.randint(0, 3)

        # Put the random number into the random location
        if self.game_grid[pos1, pos2] == 0:
            self.game_grid[pos1, pos2] = new_number
            return

    def make_move(self, move_dir, inplace=True):
        '''
        Make a move in the direction indicated.


        :param move_dir: 1 is left, 2 is down, 3 is right, and 4 is up.
        :param inplace: if inplace is True, it applies the move to the current instance of the game,
                        if inplace is False, it just checks if the move is allowed.
        :return: True if the move was valid, False if the move was invalid
        '''

        valid_move = False

        initial_game_grid = np.array(self.game_grid)

        # Left
        if move_dir == 1:
            # Rotate
            initial_game_grid = np.rot90(initial_game_grid, 2)
            initial_game_grid = self.sum_down(initial_game_grid)
            # Rotate back
            initial_game_grid = np.rot90(initial_game_grid, 2)

        # Down
        if move_dir == 2:
            # Rotate
            initial_game_grid = np.rot90(initial_game_grid, 3)
            initial_game_grid = self.sum_down(initial_game_grid)
            # Rotate back
            initial_game_grid = np.rot90(initial_game_grid, 1)

        # Right
        if move_dir == 3:
            # no rotation
            initial_game_grid = self.sum_down(initial_game_grid)

        # Up
        if move_dir == 4:
            # Rotate
            initial_game_grid = np.rot90(initial_game_grid, 1)
            initial_game_grid = self.sum_down(initial_game_grid)
            # Rotate back
            initial_game_grid = np.rot90(initial_game_grid, 3)

        if (initial_game_grid != self.game_grid).any():
            valid_move = True
        else:
            valid_move = False

        if inplace == True and valid_move == True:
            self.game_grid = initial_game_grid
            self.insert_new_number(new_game=False)
            self.total_moves = self.total_moves + 1

        return valid_move

    def sum_down(self, initial_game_grid):
        for col in range(4):

            # Remove 0s

            column = initial_game_grid[:, col][initial_game_grid[:, col] != 0]
            column = np.flip(column)
            for n in range(len(column) - 1):
                if column[n] == column[n + 1]:
                    column[n] = column[n] * 2
                    column[n + 1] = 0

            column = column[column != 0]
            for i in range(4 - len(column)):
                column = np.append(column, 0)

            initial_game_grid[:, col] = np.flip(column)
        return initial_game_grid

    def calculate_score(self, score_type="simple_sum", count_zeros=False, lost_is_zero=False):
        '''
        Calculate current score

        param: score_type

        return score
        '''
        score = 0

        if score_type == "simple_sum":
            for i in range(4):
                for j in range(4):
                    score = score + self.game_grid[i, j]

            return score

    def check_allowed_moves(self):
        '''
        Check allowed moves

        return list allowable moves
        '''

        allowed_moves = []
        for i in range(1, 5):
            allowed_move = self.make_move(i, inplace=False)
            if allowed_move:
                allowed_moves.append(i)

        return allowed_moves


    def save_game(self, replay_name, move):
        if os.path.isfile("./replays/" + replay_name + ".csv"):
            df_game_states = pd.read_csv("./replays/" + replay_name + ".csv")
            sr_game_state = pd.Series({"game_state":self.game_grid, "previous_move":move}, name=self.total_moves)
            df_game_states = df_game_states.append(sr_game_state, ignore_index=False)
            df_game_states.to_csv("./replays/" + replay_name + ".csv", index=False)
        else:
            df_game_states = pd.DataFrame(columns=["game_state", "previous_move"])
            sr_game_state = pd.Series({"game_state":self.game_grid, "previous_move":move}, name=self.total_moves)
            df_game_states = df_game_states.append(sr_game_state, ignore_index=False)
            df_game_states.to_csv("./replays/" + replay_name + ".csv", index=False)