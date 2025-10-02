import random
from collections import defaultdict
import copy

class Knucklebones:
    def __init__(self):
        self.boards = [[[0]*3 for _ in range(3)] for _ in range(2)]
        self.turn = 0
    
    def roll(self):
        return random.randint(1, 6)
    
    def place_die(self, player, roll, col):
        board = self.boards[player]
        for row in range(3):
            if board[row][col] == 0:
                board[row][col] = roll
                self._apply_destroy(player, roll, col)
                return True
        return False
    
    def _apply_destroy(self, player, roll, col):
        opp = 1 - player
        for row in range(3):
            if self.boards[opp][row][col] == roll:
                self.boards[opp][row][col] = 0
    
    def is_full(self):
        for board in self.boards:
            if all(all(cell != 0 for cell in row) for row in board):
                return True
        return False

    
    def score(self, player):
        score = 0
        # loop over each column
        for col in range(3):
            counts = defaultdict(int)
            # go down the column
            for row in range(3):
                val = self.boards[player][row][col]
                if val != 0:
                    counts[val] += 1
            # apply the Knucklebones rule: value * count^2
            for val, n in counts.items():
                score += val * (n ** 2)
        return score

    def winner(self):
        s0, s1 = self.score(0), self.score(1)
        if s0 > s1: return 0
        elif s1 > s0: return 1
        return 2
    
    def gameEndInError(self, current_player):
        opponent = 1 - current_player
        if (current_player == 0):
            return opponent, -1, self.score(1)
        else:
            return opponent, self.score(0), -1

class Player:
    def __init__(self, name="Unnamed"):
        self.name = name
        self.id = id(self)

    def choose_column(self, roll: int, my_board: list[list[int]], opp_board: list[list[int]]) -> int:
        # Should return a column (0, 1, or 2). Boards are 3x3 copies.
        raise NotImplementedError

def play_game(p1: Player, p2: Player):
    game = Knucklebones()
    players = [p1, p2]

    while not game.is_full():
        roll = game.roll()
        current = game.turn
        player = players[current]

        # give copies of the boards
        my_board = copy.deepcopy(game.boards[current])
        opp_board = copy.deepcopy(game.boards[1 - current])

        try:
            col = player.choose_column(roll, my_board, opp_board)
        except Exception:
            return game.gameEndInError(current)

        # fallback if invalid
        if col not in [0, 1, 2] or not game.place_die(current, roll, col):
            return game.gameEndInError(current)

        # switches game turn between 1 and 0
        game.turn = 1 - game.turn

    return game.winner(), game.score(0), game.score(1)

def run_tournament(players, games_per_match=1000):
    results = {p.id: {"name": p.name, "wins":0, "losses":0, "ties":0, "errors":0, "score":0} for p in players}
    numPlayers = len(players)
    totalMatches = (numPlayers * (numPlayers + 1)) // 2
    totalGames = totalMatches * games_per_match
    print(f"Running tournament with {len(players)} players, {totalMatches} matches, {games_per_match} games each ({totalGames} total games)...")
    percentageStep = 100 / totalGames
    currentPercentage = 0.0

    for i in range(len(players)):
        for j in range(i, len(players)):
            p1, p2 = players[i], players[j]
            for _ in range(games_per_match):
                w, s0, s1 = play_game(p1, p2)
                if w == 0:
                    results[p1.id]["wins"] += 1
                    results[p2.id]["losses"] += 1
                elif w == 1:
                    results[p2.id]["wins"] += 1
                    results[p1.id]["losses"] += 1
                else:
                    results[p1.id]["ties"] += 1
                    results[p2.id]["ties"] += 1
                if s0 == -1:
                    results[p1.id]["errors"] += 1
                if s1 == -1:
                    results[p2.id]["errors"] += 1
                results[p1.id]["score"] += s0
                results[p2.id]["score"] += s1
                currentPercentage += percentageStep
                print(f"Tournament progress: {currentPercentage:.2f}%", end="\r")
    return results
