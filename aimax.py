import copy
from concurrent.futures import ThreadPoolExecutor, as_completed
from logic import up, down, left, right, game_state
import os

INF = float('inf')
PERFECT_SNAKE = [[2,   4,   8,   16],
                 [256, 128, 64,  32],
                 [512, 1024,2048,4096],
                 [65536,32768,16384,8192]]
DIRECTIONS = ['up', 'down', 'left', 'right']

FLATTENED_WEIGHTS = [weight for row in PERFECT_SNAKE for weight in row]

def move(game, direction):
    if direction == 'up':
        return up(game)
    elif direction == 'down':
        return down(game)
    elif direction == 'left':
        return left(game)
    elif direction == 'right':
        return right(game)
    else:
        raise ValueError("Invalid direction!")

def snake_heuristic(board):
    flattened_board = [cell for row in board for cell in row]
    return sum(flattened_board[i] * FLATTENED_WEIGHTS[i] for i in range(len(flattened_board)))

def get_best_move_expectiminimax(board):
    depth = 2
    best_score = -INF
    best_move = DIRECTIONS[0]
    max_workers = max(4, os.cpu_count())
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for direction in DIRECTIONS:
            sim_board = copy.deepcopy(board)
            sim_board, valid, _ = move(sim_board, direction)
            if not valid:
                continue
            futures.append(executor.submit(expectiminimax, sim_board, depth, direction))
        for future in as_completed(futures):
            score, direction = future.result()
            if score > best_score:
                best_score = score
                best_move = direction

    move_functions = {
        "up": up,
        "down": down,
        "left": left,
        "right": right
    }
    return best_move, move_functions[best_move]

def expectiminimax(board, depth, direction=None):
    if game_state(board) == 'lose':
        return -INF, direction
    if depth <= 0:
        return snake_heuristic(board), direction

    if depth % 1 == 0.5:
        max_score = -INF
        for direction in DIRECTIONS:
            sim_board = copy.deepcopy(board)
            sim_board, valid, _ = move(sim_board, direction)
            if valid:
                res_score, _ = expectiminimax(sim_board, depth - 0.5, direction)
                max_score = max(max_score, res_score)
        return max_score, direction

    else:
        avg_score = 0
        open_tiles = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 0]
        for tile in open_tiles:
            board[tile[0]][tile[1]] = 2
            avg_score += (1.0 / len(open_tiles)) * expectiminimax(board, depth - 0.5, direction)[0]
            board[tile[0]][tile[1]] = 0 
        return avg_score, direction

