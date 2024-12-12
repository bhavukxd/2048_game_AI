import random
import numpy as np
from logic import *

class MonteCarlo2048AI:
    def __init__(self, grid, spm_scale_param=10, sl_scale_param=4, search_param=200):
        self.grid = grid
        self.spm_scale_param = spm_scale_param
        self.sl_scale_param = sl_scale_param
        self.search_param = search_param

    def move_up(self, grid):
        return up(grid)

    def move_down(self, grid):
        return down(grid)

    def move_left(self, grid):
        return left(grid)

    def move_right(self, grid):
        return right(grid)

    def add_random_tile(self, grid):
        return add_two(grid)

    def evaluate_move(self, board, move_function, searches_per_move, search_length):
        move_score = 0
        new_board, move_made, first_move_score = move_function(board)
        if not move_made:
            return -1 

        move_score += first_move_score
        new_board = self.add_random_tile(new_board)

        for _ in range(searches_per_move):
            simulation_board = np.copy(new_board)
            move_count = 0
            valid_game = True

            while valid_game and move_count < search_length:
                random_move = random.choice([self.move_left, self.move_right, self.move_up, self.move_down])
                simulation_board, move_made, sim_score = random_move(simulation_board)
                if move_made:
                    simulation_board = self.add_random_tile(simulation_board)
                    move_score += sim_score
                    move_count += 1
                else:
                    valid_game = False

        return move_score

    def get_search_params(self, move_number):
        searches_per_move = self.spm_scale_param * (1 + (move_number // self.search_param))
        search_length = self.sl_scale_param * (1 + (move_number // self.search_param))
        return searches_per_move, search_length

    def get_best_move(self):
        moves = {
            "up": self.move_up,
            "down": self.move_down,
            "left": self.move_left,
            "right": self.move_right
        }

        searches_per_move, search_length = self.get_search_params(move_number=0)
        best_move = None
        best_score = -1

        for move_name, move_function in moves.items():
            score = self.evaluate_move(self.grid, move_function, searches_per_move, search_length)
            if score > best_score:
                best_score = score
                best_move = move_name

        return best_move


def ai_move_monte(grid):
    ai = MonteCarlo2048AI(grid)
    best_move = ai.get_best_move()
    move_functions = {
        "up": up,
        "down": down,
        "left": left,
        "right": right
    }
    return best_move, move_functions[best_move]
