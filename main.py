import pkgutil
import inspect
import importlib
from engine import Player, run_tournament

def load_players():
    players = []
    package = "players"

    # iterate over all modules in players/
    for _, modname, _ in pkgutil.iter_modules([package]):
        module = importlib.import_module(f"{package}.{modname}")
        
        # find all Player subclasses in the module
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Player) and obj is not Player:
                players.append(obj())  # instantiate with default name
    return players

if __name__ == "__main__":
    players = load_players()
    results = run_tournament(players, games_per_match=10000)
    
    # sort leaderboard by wins
    leaderboard = sorted(results.items(), key=lambda x: x[1]["wins"], reverse=True)
    
    print("\n=== Knucklebones Tournament Results ===")
    for id, stats in leaderboard:
        total_games = stats["wins"] + stats["losses"] + stats["ties"]
        winrate = stats["wins"] / total_games * 100 if total_games else 0
        error_rate = stats["errors"] / total_games * 100 if total_games else 0
        avg_score = stats["score"]/total_games if total_games else 0
        print(f"{stats['name']:12} | Wins: {stats['wins']:3} | Losses: {stats['losses']:3} "
              f"| Ties: {stats['ties']:3} | Avg Score: {avg_score:.1f} "
              f"| Winrate: {winrate:.1f}% | Error Rate: {error_rate:.1f}%")
