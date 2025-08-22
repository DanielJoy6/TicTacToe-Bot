import numpy as np
from game import Game
from player import Player
player1 = Player("Player1", "AI", 0.99)
player2 = Player("Player2", "AI", 0.99)
players = [player1, player2]
game = Game(players)

for x in range(100000):
    game.play()
    player1.epsilon = max(0.01, player1.epsilon * 0.9995)
    if(game.winner == 0):
        if(player1.strategy == "AI"):
            player1.update_q_table(1)
        if(player2.strategy == "AI"):
            player2.update_q_table(-1)
        #print("Player 1 wins!")
    elif(game.winner == 1):
        if(player1.strategy == "AI"):
            player1.update_q_table(-1)
        if(player2.strategy == "AI"):
            player2.update_q_table(1)
        #print("Player 2 wins!")
    else:
        if(player1.strategy == "AI"):
            player1.update_q_table(0.5)
        if(player2.strategy == "AI"):
            player2.update_q_table(0.5)
        #print("It's a tie!")
    game.reset()
print(player1.epsilon)
player1.epsilon = 0
game2 = Game(players)
wins, losses, ties = 0,0,0
for x in range(100000):
    game2.play()
    if(game2.winner == 0):
        wins += 1
    elif(game2.winner == 1):
        losses += 1
    else:
        ties += 1
    game2.reset()
print(f"Wins:{wins} ({wins/1000:.2f}%), Losses: {losses} ({losses/1000:.2f}%),  Ties: {ties} ({ties/1000:2f}%)")

#for state, q_values in player1.q_table.items():
    #print(state, q_values)
#Wins: 9796 Losses: 0 Ties: 204
