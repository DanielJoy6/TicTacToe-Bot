"""Train QLPlayers"""
import sys
import random
import pickle
import numpy as np
from game import Game
from minmax_player import MinMaxPlayer
from dqn_player import DQNPlayer
from ql_player import QLPlayer
random.seed(0)
np.random.seed(0)

N = int(sys.argv[1])
decay = (0.05 / 1) ** (1.0 / N)   # ≈ 0.9999089

alpha_decay = (0.01 / 0.1) ** (1.0 / max(1, N))
#q_table = {}
print("Initialized Players")

def convert_q_table_negate(q_table):
    """Helper function to invert q table depending on symbol"""
    new_q = {}
    for key, qvals in q_table.items():
        neg_key = tuple(-x for x in key)  # invert perspective
        new_q[neg_key] = qvals.copy()
    return new_q



def train(player1, player2, training_rounds):
    """Trains Q learning bots"""
    players = [player1, player2]
    game = Game(players, "train")
    print(f"Training for {training_rounds} rounds")
    for _ in range(training_rounds):
        game.play()
        if isinstance(player1, QLPlayer):
            player1.epsilon = max(0.05, player1.epsilon * decay)
            player1.alpha = max(0.01, player1.alpha * alpha_decay)
        if isinstance(player2, QLPlayer):
            player2.epsilon = max(0.05, player2.epsilon * decay)
            player2.alpha = max(0.01, player2.alpha * alpha_decay)
        game.reset()
    if isinstance(player1, QLPlayer):
        with open("QLTableX", 'wb') as file:
            pickle.dump(player1.Q_X, file)
        with open("QLTableO", 'wb') as file:
            pickle.dump(player1.Q_O, file)
    if isinstance(player1, DQNPlayer):
        with open('DQNMemory.pkl', 'wb') as f:
            pickle.dump(player1.memory, f)

    print("Training complete!\n")


def evaluate(player1, player2, rounds):
    """Evaluates two players, no updating q tables"""
    players = [player1, player2]
    if isinstance(player1, QLPlayer):
        player1.epsilon = 0
    if isinstance(player2, QLPlayer):
        player2.epsilon = 0
    game2 = Game(players, "evaluation")
    print(f"Evaluating for {rounds} rounds")
    wins, losses, ties = 0, 0, 0
    for _ in range(rounds):
        game2.play()
        if game2.winner == 1:
            wins += 1
        elif game2.winner == -1:
            losses += 1
        else:
            ties += 1
        game2.reset()
    print("Done evaluating! Record:")
    print(
        f"Wins:{wins} ({wins/rounds*100:.2f}%), Losses: {losses}({losses/rounds*100:.2f}%),  Ties: {ties} ({ties/rounds*100:2f}%)"
    )


first_player = QLPlayer("Player1", 0.99, 0.1, 0.95, symbol=1)
second_player = MinMaxPlayer("Player2", symbol=-1)
if len(sys.argv) == 1:
    train(first_player, second_player, 1000)
else:
    train(first_player, second_player, int(sys.argv[1]))

if isinstance(first_player, QLPlayer):
    first_player.states.clear()
if isinstance(second_player, QLPlayer):
    second_player.states.clear()

evaluate(first_player, second_player, 500)

first_player = DQNPlayer("Player1", symbol=1)
second_player = MinMaxPlayer("Player2", symbol=-1)
train(first_player, second_player, 5000)
evaluate(first_player, second_player, 500)
