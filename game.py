#Game class
import numpy
class Game:
    def __init__(self, players):
        self.players = players
        self.board = [" " for x in range(9)]
        self.gameOver = False
        self.winner = ""
    def printBoard(self):
        for x in range(3):
            print("|", end="")
            for y in range(3):
                print(self.board[x*3+y], end="")
                print("|", end="")
            print("\n---------")
    def playGame(self):
        while(True):
            move = self.players[0].makeMove(self.board)
            self.board[move] = "X"
            self.checkForWin()
            if(self.gameOver):
                break
            move = self.players[1].makeMove(self.board)
            self.board[move] = "O"
            self.checkForWin()
            if(self.gameOver):
                break
    def checkForWin(self):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for (i, j, k) in win_conditions:
            if(self.board[i] != " " and self.board[i] == self.board[j] == self.board[k]):
                if(self.board[i] == "X"):
                    self.winner = 0
                    self.gameOver = True
                else:
                    self.winner = 1
                    self.gameOver = True
        if " " not in self.board:
            self.gameOver = True
            self.winner = 2
        return

    def reset(self):
        self.board = [" " for x in range(9)]
        self.gameOver = False
        self.winner = ""
