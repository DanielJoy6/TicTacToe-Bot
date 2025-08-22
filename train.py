from game import Game
from player import Player
import numpy as np


player1 = Player("Agent1", "AI", 1)
player2 = Player("Agent2", "AI", 1)
game = Game([player1, player2])

for episode in range(200000):
    game.play()

    # Rewards
    if game.winner == 0:
        player1.update_q_table(1)
        player2.update_q_table(-1)
    elif game.winner == 1:
        player1.update_q_table(-1)
        player2.update_q_table(1)
    else:
        player1.update_q_table(0.5)
        player2.update_q_table(0.5)

    # Decay epsilon
    player1.epsilon = max(0.01, player1.epsilon * 0.995)
    player2.epsilon = max(0.01, player2.epsilon * 0.995)

    game.reset()

# Save trained Q-table
np.save("q_table.npy", p1.q_table)
print("Training complete")
