"""Monte Carlo Tree Search (MCTS) Player"""
from base_player import Player
import math
import random

class MCTSNode:
    def __init__(self, board, parent, move, symbol):
        self.board = board[:]
        self.parent = parent
        self.move = move
        self.symbol = symbol
        self.children = []
        self.visits = 0
        self.value = 0

    def expand(self):
        validMoves = [i for i, v in enumerate(self.board) if v == 0]
        for mv in validMoves:
            new_board = self.board[:]
            new_board[mv] = self.symbol
            self.children.append(MCTSNode(new_board, self, mv, -self.symbol))

    def best_child(self, c=1.4):
        return max(self.children, key=lambda n: (n.value / (n.visits + 1e-9)) + c * math.sqrt(math.log(self.visits + 1) / (n.visits + 1e-9)))

class MCTSPlayer(Player):
    def __init__(self, name, symbol, iterations=500):
        super().__init__(name)
        self.symbol = symbol
        self.iterations = iterations

    def makeMove(self, board, gametype):
        root = MCTSNode(board, None, None, self.symbol)
        root.expand()

        for _ in range(self.iterations):
            leaf = self.select(root)
            reward = self.simulate(leaf.board, leaf.symbol)
            while leaf:
                leaf.visits += 1
                leaf.value += reward
                reward = -reward
                leaf = leaf.parent

        best = max(root.children, key=lambda n: n.visits)
        return best.move

    def select(self, node):
        while node.children:
            node = node.best_child()
        if node.visits > 0:
            node.expand()
            if node.children:
                return random.choice(node.children)
        return node

    def simulate(self, board, symbol):
        temp = board[:]
        current = symbol
        while True:
            res = self.checkForWin(temp)
            if res is not None:
                return res
            moves = [i for i, v in enumerate(temp) if v == 0]
            mv = random.choice(moves)
            temp[mv] = current
            current = -current


    def checkForWin(self, board):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in wins:
            if board[a] != 0 and board[a] == board[b] == board[c]:
                return 1 if board[a] == self.symbol else -1
        if 0 not in board:
            return 0
        return None

    def reset(self):
        pass
