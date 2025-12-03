"""Testing Player Implementations"""
import time
from game import Game
from minmax_player import MinMaxPlayer
from random_player import RandomPlayer
from minmax_alphabeta_player import MinMaxAlphaBetaPlayer

first_player = MinMaxAlphaBetaPlayer("Player1", symbol=1)
second_player = RandomPlayer("Player2", symbol=-1)

players = [first_player, second_player]
game = Game(players, "evaluate")
wins, losses,ties, rounds = 0,0,0, 300
start = time.time()
for _ in range(rounds):
    print(_)
    game.play()
    if game.winner == 1:
        wins += 1
    elif game.winner == -1:
        losses += 1
    else:
        ties += 1
    game.reset()
print("Done evaluating! Record:")
print(
    f"Wins:{wins} ({wins/rounds*100:.2f}%), Losses: {losses} ({losses/rounds*100:.2f}%),  Ties: {ties} ({ties/rounds*100:2f}%)"
)
end = time.time()
print("Time taken:", end-start, "seconds")