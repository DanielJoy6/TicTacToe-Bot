"""Player that employs MinMax Algorithm"""
from base_player import Player

class MinMaxPlayer(Player):
    """
    Player that employs Min-Max Algorithm
    """
    def __init__(self, name, symbol):
        super().__init__(name)
        self.symbol = symbol
    def makeMove(self, board, gametype):
        #print("----------MINMAX DEBUG----------")
        best_score = -2
        best_move = None
        validMoves = [x for x in range(len(board)) if board[x] == 0]
        for move in validMoves:
            board[move] = self.symbol
            score = self.MinMax(board, self.symbol*-1)
            board[move] = 0
            #print("Move:", move, "score:", score)
            if(score > best_score):
                best_score = score
                best_move = move
        #print("----------MINMAX DEBUG----------")
        return best_move
    
    def MinMax(self, board, symbol):
        result = self.checkForWin(board)
        if result is not None:
            return result
        validMoves = [x for x in range(len(board)) if board[x] == 0]
        if symbol == self.symbol:
            best = -2
            for move in validMoves:
                board[move] = symbol
                score = self.MinMax(board, symbol*-1)
                board[move] = 0
                if score == 1:
                    return 1
                best = max(best, score)
            return best
        else:
            best = 2
            for move in validMoves:
                board[move] = symbol
                score = self.MinMax(board, symbol*-1)
                board[move] = 0
                if score == -1:
                    return -1
                best = min(best, score)
            return best
    
    def checkForWin(self, board):
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
            if board[i] != 0 and board[i] == board[j] == board[k]:
                if board[i] == self.symbol:
                    return 1
                else:
                    return -1
        if 0 not in board:
            return 0
        return
    
    def reset(self):
        pass