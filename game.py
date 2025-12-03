import random
from ql_player import QLPlayer
# Game class
class Game:
    def __init__(self, players, gametype):
        self.players = players
        self.board = [0 for x in range(9)]
        self.gameOver = False
        self.winner = 0
        self.gametype = gametype

    def printBoard(self):
        for x in range(3):
            print("|", end="")
            for y in range(3):
                print(self.board[x * 3 + y], end="")
                print("|", end="")
            print("\n---------")

    def play(self):
        # Randomly choose starting player
        turn_idx = 0 if random.random() < 0.5 else 1
        
        while not self.gameOver:
            current_player = self.players[turn_idx]
            other_player = self.players[1 - turn_idx]
            
            # 1. GET MOVE
            move = current_player.makeMove(self.board, self.gametype)
            #print("Player move:", move)
            self.board[move] = current_player.symbol
            #self.printBoard()

            # 2. CHECK FOR WIN/DRAW
            self.checkForWin()
            
            reward_current = 0
            reward_other = 0
            game_ended = False

            if self.winner != 0 and self.winner != 2:
                reward_current = 1
                reward_other = -1
                game_ended = True
            elif self.winner == 2:
                # Draw
                reward_current = 0.5 # or 0, depending on preference
                reward_other = 0.5
                game_ended = True
            
            # 3. PERFORM UPDATES
            if self.gametype == "train":
                # If the game ended, BOTH players get updated immediately
                if game_ended:
                    if isinstance(current_player, QLPlayer):
                        current_player.update_q_table(reward_current, self.board)
                    if isinstance(other_player, QLPlayer):
                        other_player.update_q_table(reward_other, self.board)
                
                else:
                    if isinstance(other_player, QLPlayer):
                        other_player.update_q_table(0, self.board)

            if game_ended:
                break
                
            # Switch turn
            turn_idx = 1 - turn_idx

    def checkForWin(self):
        win_conditions = [
            (0, 1, 2), #Rows
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6), #Columns
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8), #Diagonal
            (2, 4, 6),
        ]
        for i, j, k in win_conditions:
            if self.board[i] != 0 and self.board[i] == self.board[j] == self.board[k]:
                if self.board[i] == 1:
                    self.winner = 1
                else:
                    self.winner = -1
                self.gameOver = True
        if(self.gameOver):
            return
        if 0 not in self.board:
            self.gameOver = True
            self.winner = 2
        return
    
    def checkForWinNoWinner(self):
        win_conditions = [
            (0, 1, 2), #Rows
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6), #Columns
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8), #Diagonal
            (2, 4, 6),
        ]
        for i, j, k in win_conditions:
            if self.board[i] != 0 and self.board[i] == self.board[j] == self.board[k]:
                if self.board[i] == 1:
                    return 0
                else:
                    return 1
        if 0 not in self.board:
            return 2
        return -1

    def reset(self):
        self.board = [0 for x in range(9)]
        self.gameOver = False
        self.winner = 0
