"""Player that moves randomly"""
import random
from base_player import Player

class RandomPlayer(Player):
    """
    Player that moves randomly
    """
    def __init__(self, name, symbol):
        super().__init__(name)
        self.symbol = symbol

    def makeMove(self, board, gametype):
        validMoves = [x for x in range(len(board)) if board[x] == 0]
        return random.choice(validMoves)
    def reset(self):
        pass