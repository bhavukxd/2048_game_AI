import numpy as np
import logic

class Game2048AI:
    def __init__(self, grid):
        self.grid = np.array(grid)

    def slide_and_merge_left(self, grid):
        new_grid = []
        score = 0
        for row in grid:
            non_zero_tiles = row[row != 0] 
            merged_row = []
            skip = False
            for i in range(len(non_zero_tiles)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(non_zero_tiles) and non_zero_tiles[i] == non_zero_tiles[i + 1]:
                    merged_row.append(non_zero_tiles[i] * 2)
                    score += non_zero_tiles[i] * 2
                    skip = True
                else:
                    merged_row.append(non_zero_tiles[i])
            merged_row.extend([0] * (len(row) - len(merged_row)))
            new_grid.append(merged_row)
        return np.array(new_grid), score

    def move_left(self, grid):
        return self.slide_and_merge_left(grid)

    def move_right(self, grid):
        reversed_grid = np.fliplr(grid)
        new_grid, score = self.slide_and_merge_left(reversed_grid)
        return np.fliplr(new_grid), score

    def move_up(self, grid):
        transposed_grid = grid.T
        new_grid, score = self.slide_and_merge_left(transposed_grid)
        return new_grid.T, score

    def move_down(self, grid):
        transposed_grid = np.fliplr(grid.T)
        new_grid, score = self.slide_and_merge_left(transposed_grid)
        return np.fliplr(new_grid).T, score

    def get_best_move(self):
        moves = {
            "left": self.move_left(self.grid),
            "right": self.move_right(self.grid),
            "up": self.move_up(self.grid),
            "down": self.move_down(self.grid)
        }
        mv1 = {
            "left": logic.left,
            "right": logic.right,
            "up": logic.up,
            "down": logic.down
        }

        best_move = None
        best_score = -1
        best_grid = None
        
        for move, (new_grid, score) in moves.items():
            if not np.array_equal(new_grid, self.grid):
                if score > best_score:
                    best_score = score
                    best_move = move
                    best_grid = new_grid
                    
        return best_move,mv1[best_move]
def ai_move(grid):
    ai = Game2048AI(grid)
    best_move,movefc= ai.get_best_move()
    # print("Best move:", best_move)
    return best_move,movefc
