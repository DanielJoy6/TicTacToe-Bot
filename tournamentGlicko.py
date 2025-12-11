import pickle
import time
import math
import warnings
from game import Game
from random_player import RandomPlayer
from minmax_player import MinMaxPlayer
from minmax_alphabeta_player import MinMaxAlphaBetaPlayer
from monteCarlo_player import MCTSPlayer
from dqn_player import DQNPlayer
from ql_player import QLPlayer

warnings.filterwarnings("ignore", category=UserWarning)

q = math.log(10) / 400
DEFAULT_RATING = 1500
DEFAULT_RD = 350

def g(RD):
    return 1 / math.sqrt(1 + (3 * q * q * RD * RD) / (math.pi * math.pi))

def E(r, r_j, RD_j):
    return 1 / (1 + 10 ** (-g(RD_j)*(r - r_j) / 400))

def update_glicko(r, RD, matches):
    if not matches:
        RD = min(350, math.sqrt(RD**2 + 50**2))
        return r, RD
    v_inv = 0
    for r_j, RD_j, score in matches:
        E_j = E(r, r_j, RD_j)
        v_inv += (g(RD_j)**2) * E_j * (1 - E_j)
    v = 1 / (q * q * v_inv)
    delta_sum = 0
    for r_j, RD_j, score in matches:
        E_j = E(r, r_j, RD_j)
        delta_sum += g(RD_j) * (score - E_j)

    delta = v * q * delta_sum
    RD_new = 1 / math.sqrt((1 / RD**2) + (1 / v))
    r_new = r + (q / ((1 / RD**2) + (1 / v))) * delta_sum
    return r_new, RD_new

def run_tournament(players, rounds=100):
    ratings = {p.name: DEFAULT_RATING for p in players}
    deviations = {p.name: DEFAULT_RD for p in players}

    for player in players:
        if isinstance(player, QLPlayer):
            with open("QLTableX", 'rb') as file:
                player.Q_X = pickle.load(file)
            with open("QLTableO", 'rb') as file:
                player.Q_O = pickle.load(file)
        if isinstance(player, DQNPlayer):
            with open('DQNMemory.pkl', 'rb') as f:
                player.memory = pickle.load(f)

    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            p1 = players[i]
            p1.symbol = 1
            p2 = players[j]
            p2.symbol = -1

            p1_matches = []
            p2_matches = []

            for _ in range(rounds):
                game = Game([p1, p2], "evaluate")
                game.play()

                if game.winner == p1.symbol:
                    score1, score2 = 1, 0
                elif game.winner == p2.symbol:
                    score1, score2 = 0, 1
                else:
                    score1, score2 = 0.5, 0.5

                p1_matches.append((ratings[p2.name], deviations[p2.name], score1))
                p2_matches.append((ratings[p1.name], deviations[p1.name], score2))
                game.reset()

            ratings[p1.name], deviations[p1.name] = update_glicko(
                ratings[p1.name],
                deviations[p1.name],
                p1_matches
            )
            ratings[p2.name], deviations[p2.name] = update_glicko(
                ratings[p2.name],
                deviations[p2.name],
                p2_matches
            )

    return ratings, deviations


def print_rankings(ratings, deviations):
    print("\nFinal Rankings (Glicko):")
    ranked = sorted(ratings.items(), key=lambda x: x[1], reverse=True)

    for name, rating in ranked:
        RD = deviations[name]
        print(f"{name:20}  {rating:.1f}   RD={RD:.1f}")

players = [
    RandomPlayer("Random", 1),
    MinMaxPlayer("MinMax", 1),
    MinMaxAlphaBetaPlayer("AlphaBeta", 1),
    QLPlayer("QLPlayer", 0.99, 0.1, 0.95, symbol=1),
    DQNPlayer("DQNPlayer", symbol=1),
    MCTSPlayer("Monte Carlo", symbol=1),
]

start = time.time()
rounds = 250

ratings, deviations = run_tournament(players, rounds=rounds)
print_rankings(ratings, deviations)
end = time.time()
print(f"Time taken to run {rounds}-round tournament: {end-start:.2f} seconds")
