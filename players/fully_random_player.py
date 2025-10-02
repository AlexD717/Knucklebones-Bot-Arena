from engine import Player
import random

class RandomPlayer(Player):
    def __init__(self, name="Fully Random"):
        super().__init__(name)

    def choose_column(self, roll, my_board, opp_board):
        return random.choice([0, 1, 2])
