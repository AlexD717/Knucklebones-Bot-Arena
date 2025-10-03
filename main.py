from engine import Player, run_tournament
import pkgutil
import inspect
import importlib
import multiprocessing
import psutil
from collections import defaultdict

games_per_match = 10000

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

def worker(players, games):
    return run_tournament(players, games)

def merge_results(results_list):
    merged = defaultdict(lambda: {"wins":0, "losses":0, "ties":0, "errors":0, "score":0, "name":""})
    for result in results_list:
        for pid, stats in result.items():
            if not merged[pid]["name"]:
                merged[pid]["name"] = stats["name"]
            merged[pid]["wins"]   += stats["wins"]
            merged[pid]["losses"] += stats["losses"]
            merged[pid]["ties"]   += stats["ties"]
            merged[pid]["errors"] += stats["errors"]
            merged[pid]["score"]  += stats["score"]
    return merged

if __name__ == "__main__":
    players = load_players()

    num_workers = psutil.cpu_count(logical=True)
    if num_workers == None or num_workers < 1:
        num_workers = 1
    
    games_per_worker = int(games_per_match) // num_workers
    num_players = len(players)
    total_matches = (num_players * (num_players + 1)) // 2

    print(f"Running tournament with {len(players)} players, {total_matches} matches, {games_per_match} games each ({total_matches*games_per_match} total games)...")
    print(f"Running tournament with {num_workers} workers...")

    with multiprocessing.Pool(num_workers) as pool:
        results_list = pool.starmap(worker, [(players, games_per_worker) for _ in range(num_workers)])

    # merge all worker results
    results = merge_results(results_list)

    # sort leaderboard by wins
    leaderboard = sorted(results.items(), key=lambda x: x[1]["wins"], reverse=True)

    print("\n=== Knucklebones Tournament Results ===")
    for pid, stats in leaderboard:
        total_games = int(stats["wins"]) + int(stats["losses"]) + int(stats["ties"])
        winrate = int(stats["wins"]) / total_games * 100 if total_games else 0
        error_rate = int(stats["errors"]) / total_games * 100 if total_games else 0
        avg_score = int(stats["score"]) / total_games if total_games else 0
        print(f"{stats['name']:12} | Wins: {stats['wins']:3} | Losses: {stats['losses']:3} "
              f"| Ties: {stats['ties']:3} | Avg Score: {avg_score:.1f} "
              f"| Winrate: {winrate:.1f}% | Error Rate: {error_rate:.1f}%")
