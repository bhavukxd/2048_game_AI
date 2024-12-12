import random
import numpy as np
import logic
import constants as c
import time
from tkinter import Frame, Label, CENTER,messagebox
from ai1 import ai_move
from aim import ai_move_monte
from aip import ai_move_priority
from aimax import get_best_move_expectiminimax
from pynput.keyboard import Key, Listener
import matplotlib.pyplot as plt 
import json


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.score = 0
        self.mode = None
        self.update_title()
        self.master.bind("<Key>", self.key_down)
        self.highest_tile = 2
        self.seed = 342
        random.seed(self.seed)
        np.random.seed(self.seed)
        self.count=0
        self.over_play=False
        self.run = False
        self.moves=[]
        self.scores_over_time = []
        self.highest_tiles_over_time = []
        self.ai_list = [ai_move, ai_move_priority,ai_move_monte,get_best_move_expectiminimax]
        self.mode_names = ["Manual","Heuristic","Priority","Monte_Carlo","Minmax"]
        self.current = int(input("""
        Enter the game mode:
        1 for Manual
        2 for AI based-1 (Heuristic Based)
        3 for AI based 2 (Priority)
        4 for AI based 3 (Monte Carlo)
        5 for AI based 4 (Minmax)
        """))
        self.mode = self.mode_names[self.current-1]
        self.update_title()
        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }
        self.manual_moves =  {
            logic.down:"down",
            logic.left:"left",
            logic.right:"right",
            logic.up:"up"
        }
        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()
        self.listener = Listener(
            on_press=self.on_key_press,
            on_release=lambda *args: None 
        )
        self.listener.start()
        self.mainloop()

    def update_highest_tile(self):
        self.highest_tile = max(self.highest_tile, max(max(row) for row in self.matrix))
        self.update_title()

    def update_title(self):
        self.master.title(f'2048 - Score:{self.score} Mode:{self.mode}')

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(row=i, column=j, padx=c.GRID_PADDING, pady=c.GRID_PADDING)
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=4,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def nextMove(self):
        best_move,movefc = self.ai_list[self.current - 2](self.matrix)
        self.matrix, done,score_i = movefc(self.matrix)
        self.moves.append(best_move)
        self.count+=1
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            self.score+=score_i
            self.scores_over_time.append(self.score)
            self.update_title()
            self.update_highest_tile()
            self.highest_tiles_over_time.append(self.highest_tile)
            self.update_grid_cells()
            if logic.game_state(self.matrix) == 'win' and self.over_play==False:
                messagebox.showinfo("Winner", "You have reached 2048")
                print(f"Total Score: {self.score}")
                print(f"Highest Tile: {self.highest_tile}")
                print(f"Total Turns: {self.count}")
                self.end_game()
                return

            if logic.game_state(self.matrix) == 'lose':
                self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.end_game()
                self.cont = False

                return
        time.sleep(0.1)

    def end_game(self):
        print(f"Total Score: {self.score}")
        print(f"Highest Tile: {self.highest_tile}")
        print(f"Total Turns: {self.count}")
        print(f"Moves: {self.moves}")
        self.save_data()
        self.plot_game_statistics()
        self.over_play = True
    
    def plot_game_statistics(self):
        plt.figure(figsize=(12, 6))

        plt.subplot(2, 2, 1)
        plt.title("Score Progression Over Time")
        plt.plot(self.scores_over_time, label="Score", color="blue")
        plt.xlabel("Moves")
        plt.ylabel("Score")
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.title("Highest Tile Progression Over Time")
        plt.plot(self.highest_tiles_over_time, label="Highest Tile", color="orange")
        plt.xlabel("Moves")
        plt.ylabel("Highest Tile")
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.title("Move Count")
        move_counts = {move: self.moves.count(move) for move in set(self.moves)}
        plt.bar(move_counts.keys(), move_counts.values(), color="green")
        plt.xlabel("Moves")
        plt.ylabel("Frequency")

        plt.subplot(2, 2, 4)
        plt.title("Game Summary")
        plt.text(0.5, 0.8, f"Final Score: {self.score}", ha="center")
        plt.text(0.5, 0.6, f"Highest Tile: {self.highest_tile}", ha="center")
        plt.text(0.5, 0.4, f"Total Turns: {self.count}", ha="center")
        plt.axis("off")

        plt.tight_layout()
        plt.show()

    def save_data(self):
        file_path = self.mode+".json"
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
                data = {}
        if f"{self.seed}" not in dict(data):
            data[self.seed]={
            "Final_Score":self.score,
            "Highest_Tile":self.highest_tile,
            "Move_Count":self.count,
            "Moves":self.moves}
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

    def manual(self, event):
        key = event.keysym
        if key == c.KEY_QUIT:
            exit()
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
        elif key in self.commands:
            self.matrix, done,score_i = self.commands[key](self.matrix)
            self.score+=score_i
            self.count+=1
            self.moves.append(self.manual_moves[self.commands[key]])
            self.update_title()
            if done:
                self.matrix = logic.add_two(self.matrix)
                self.history_matrixs.append(self.matrix)
                self.update_highest_tile()
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'win' and self.over_play==False:
                    messagebox.showinfo("Winner", "You have reached 2048")
                    print(f"Total Score: {self.score}")
                    print(f"Highest Tile: {self.highest_tile}")
                    print(f"Total Turns: {self.count}")
                    self.save_data()
                    self.over_play = True
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    print(f"Total Score: {self.score}")
                    print(f"Highest Tile: {self.highest_tile}")
                    print(f"Total Turns: {self.count}")
                    if(self.over_play==False):
                        self.save_data()

    def ai_based(self, event):
        key = event.keysym
        self.run = True
        if key == c.KEY_QUIT:
            self.run = False
            exit()
        if key == c.KEY_START:
            self.cont = True
            while self.cont and self.run:
                self.nextMove()

    def key_down(self, event):
        if self.current == 1:
            self.manual(event)
        else:
            self.ai_based(event)
    
    def on_key_press(self,key):
        if(key==Key.backspace and self.current > 1):
            self.run = True
            self.cont = True
            while self.cont and self.run:
                self.nextMove()


game_grid = GameGrid()
