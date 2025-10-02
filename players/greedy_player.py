from engine import Player, Knucklebones
import copy

class GreedyPlayer(Player):
    def __init__(self, name="Greedy"):
        super().__init__(name)

    def choose_column(self, roll, my_board, opp_board):
        # simulate each option on my board copy
        best_col, best_gain = -1, -1

        # build a temp game with both boards so scoring works
        for col in range(3):
            temp_game = Knucklebones()
            temp_game.boards[0] = copy.deepcopy(my_board)
            temp_game.boards[1] = copy.deepcopy(opp_board)

            if temp_game.place_die(0, roll, col):  # simulate my move
                gain = temp_game.score(0)  # just check resulting score
                if gain > best_gain:
                    best_gain = gain
                    best_col = col

        if (best_col == -1):
            print("GreedyPlayer found no valid moves, defaulting to column 0")
            print(my_board)
            print(opp_board)
            return 0

        return best_col
