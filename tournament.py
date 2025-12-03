import pickle
import time
import warnings
from game import Game
from random_player import RandomPlayer
from minmax_player import MinMaxPlayer
from minmax_alphabeta_player import MinMaxAlphaBetaPlayer
from monteCarlo_player import MCTSPlayer
from dqn_player import DQNPlayer
from ql_player import QLPlayer

warnings.filterwarnings("ignore", category=UserWarning)

def update_elo(ratingA, ratingB, scoreA, K=32):
    expectedA = 1 / (1 + 10 ** ((ratingB - ratingA) / 400))
    new_ratingA = ratingA + K * (scoreA - expectedA)
    return new_ratingA

def run_tournament(players, rounds=100):
    # Initialize ELO scores for all players
    elo = {p.name: 1000 for p in players}
    for player in players:
        if isinstance(player, QLPlayer):
            with open("QLTableX", 'rb') as file:
                player.Q_X = pickle.load(file)
            with open("QLTableO", 'rb') as file:
                player.Q_O = pickle.load(file)
        if isinstance(player, DQNPlayer):
            with open('DQNMemory.pkl', 'rb') as f:
                player.memory = pickle.load(f)
    # Round robin
    for i in range(len(players)):
        for j in range(i + 1, len(players)):  # avoid duplicate matches
            p1 = players[i]
            p1.symbol = 1
            p2 = players[j]
            p2.symbol = -1
            
            # Play `rounds` games between these two players
            for _ in range(rounds):
                game = Game([p1, p2], "evaluate")
                game.play()

                # Scoring for ELO
                if game.winner == p1.symbol:
                    elo[p1.name] = update_elo(elo[p1.name], elo[p2.name], 1)
                    elo[p2.name] = update_elo(elo[p2.name], elo[p1.name], 0)
                elif game.winner == p2.symbol:
                    elo[p1.name] = update_elo(elo[p1.name], elo[p2.name], 0)
                    elo[p2.name] = update_elo(elo[p2.name], elo[p1.name], 1)
                else:
                    elo[p1.name] = update_elo(elo[p1.name], elo[p2.name], 0.5)
                    elo[p2.name] = update_elo(elo[p2.name], elo[p1.name], 0.5)

                game.reset()

    return elo

def print_rankings(elo):
    print("\nFinal Rankings (ELO):")
    ranked = sorted(elo.items(), key=lambda x: x[1], reverse=True)
    for name, rating in ranked:
        print(f"{name:20}  {rating:.1f}")

players = [
    RandomPlayer("Random", 1),
    MinMaxPlayer("MinMax", 1),
    MinMaxAlphaBetaPlayer("AlphaBeta", 1),
    QLPlayer("QLPlayer", 0.99, 0.1, 0.95, symbol=1),
    DQNPlayer("DQNPlayer", symbol=1),
    MCTSPlayer("Monte Carlo", symbol=1)
]
start = time.time()
rounds = 500


elo = run_tournament(players, rounds=rounds)
print_rankings(elo)
end = time.time()
print(f"Time taken to run {rounds}-round tournament: {end-start:.2f} seconds")
