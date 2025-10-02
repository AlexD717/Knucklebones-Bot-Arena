from engine import Player
import random

class RandomPlayer(Player):
    def __init__(self, name="Legal Random"):
        super().__init__(name)

    def choose_column(self, roll, my_board, opp_board):
        validCols = []
        for col in range(3):
            if my_board[0][col] == 0 or my_board[1][col] == 0 or my_board[2][col] == 0:
                validCols.append(col)

        if (len(validCols) > 0):
            return random.choice(validCols)
        else:
            print("RandomPlayer found no valid moves, defaulting to column 0")
            return 0
