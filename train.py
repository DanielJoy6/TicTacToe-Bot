import numpy as np
from game import Game
from player import Player
player1 = Player("Player1", "AI", 0.99, 0.5, 0.7)
player2 = Player("Player2", "AI", 0.99, 0.5, 0.7)
print("Initialized Players")
def train(player1, player2, training_rounds):
    players = [player1, player2]
    game = Game(players)
    print(f"Training for {training_rounds} rounds")
    for x in range(training_rounds):
        game.play()
        player1.epsilon = max(0.01, player1.epsilon * 0.999)
        player2.epsilon = max(0.01, player2.epsilon * 0.999)
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
                player1.update_q_table(-0.1)
            if(player2.strategy == "AI"):
                player2.update_q_table(-0.1)
            #print("It's a tie!")
        game.reset()
    print("Training complete!\n")
def evaluate(player1, player2, rounds, strategy):
    players = [player1, player2]
    player1.epsilon = 0
    if(strategy == "random"):
        print("Evaluating against an opponent who moves randomly...")
        player2.strategy = "random"
    elif(strategy == "AI"):
        print("\nEvaluating against itself...")
        player2.strategy = "AI"
        player2.epsilon = 0
    game2 = Game(players)
    wins, losses, ties = 0,0,0
    for x in range(rounds):
        game2.play()
        if(game2.winner == 0):
            wins += 1
        elif(game2.winner == 1):
            losses += 1
        else:
            ties += 1
        game2.reset()
    print("Done evaluating! Record:")
    print(f"Wins:{wins} ({wins/1000:.2f}%), Losses: {losses} ({losses/1000:.2f}%),  Ties: {ties} ({ties/1000:2f}%)")



train(player1, player2, 100000)

evaluate(player1, player2, 100000, "random")
evaluate(player1, player2, 100000, "AI")

train(player1, player2, 100000)

evaluate(player1, player2, 100000, "random")
evaluate(player1, player2, 100000, "AI")
