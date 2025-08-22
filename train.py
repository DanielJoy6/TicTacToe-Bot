import numpy as np
from game import Game
from player import Player
player1 = Player("Player1", "AI", 0.99, 0.1, 0.9)
player2 = Player("Player2", "AI", 0.99, 0.1, 0.9)
q_table = {}
print("Initialized Players")
def train(player1, player2, training_rounds):
    players = [player1, player2]
    game = Game(players)
    print(f"Training for {training_rounds} rounds")
    for x in range(training_rounds):
        game.play()
        player1.epsilon = max(0.005, player1.epsilon * 0.999)
        player2.epsilon = max(0.005, player2.epsilon * 0.999)
        if(game.winner == 0):
            if(player1.strategy == "AI"):
                player1.update_q_table(1)
            if(player2.strategy == "AI"):
                player2.update_q_table(-5)
            #print("Player 1 wins!")
        elif(game.winner == 1):
            if(player1.strategy == "AI"):
                player1.update_q_table(-5)
            if(player2.strategy == "AI"):
                player2.update_q_table(1)
            #print("Player 2 wins!")
        else:
            if(player1.strategy == "AI"):
                player1.update_q_table(-0.2)
            if(player2.strategy == "AI"):
                player2.update_q_table(-0.2)
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
    print(f"Wins:{wins} ({wins/rounds*100:.2f}%), Losses: {losses} ({losses/rounds*100:.2f}%),  Ties: {ties} ({ties/rounds*100:2f}%)")



train(player1, player2, 100000)

evaluate(player1, player2, 1000000, "random")
evaluate(player1, player2, 10000, "AI")
