import numpy as np
import random
class Player:
    def __init__(self, name, strategy, epsilon, alpha, gamma):
        self.name = name
        self.strategy = strategy
        self.epsilon = epsilon
        self.q_table = {}
        self.states = []
        self.alpha = alpha
        self.gamma = gamma
        self.canon_cache = {}

    def canonical(self, board):
        board_tuple = tuple(board)
        if board_tuple in self.canon_cache:
            return self.canon_cache[board_tuple]

        board_np = np.array(board).reshape(3, 3)
        transformations = []
        for i in range(4):
            rotated = np.rot90(board_np, i)
            transformations.append(rotated)
            transformations.append(np.fliplr(rotated))
        canon = min(tuple(t.flatten()) for t in transformations)
        self.canon_cache[board_tuple] = canon
        return canon

    def makeMove(self, board, symbol):
        validMoves = [] #board = [" ", "X", "O", "X", "O"...]
        for x in range(len(board)):
            if(board[x] == " "):
                validMoves.append(x)
        if(self.strategy == "human"):
            print("Your valid moves are:", validMoves)
            print("Where would you like to move?")
            move = int(input())
            return move
        elif(self.strategy == "random"):
            return random.choice(validMoves)
        elif(self.strategy == "AI"):
            state = self.canonical(board)
            move_index = 0
            if state not in self.q_table:
                self.q_table[state] = [0.0 for _ in range(9)]
            masked_q_values = np.array([
                self.q_table[state][i] if i in validMoves else -np.inf
                for i in range(9)
            ])
            if(random.random() < self.epsilon):
                move = random.choice(validMoves)
            else:
                move = int(np.argmax(masked_q_values))
            next_board = board.copy()
            next_board[move] = symbol
            next_state = self.canonical(next_board)
            self.states.append((state, move, next_state))
            return move
    '''
    def updateQTable(self, reward):
        for(state, action_index) in self.states:
            self.q_table[state][action_index] += reward
        self.states.clear()
    '''
    #New Version
    def update_q_table(self, reward):
        for (state, action_index, next_state) in self.states:
            if next_state not in self.q_table:
                self.q_table[next_state] = [0.0 for _ in range(9)]
            max_future_q = max(self.q_table[next_state])
            self.q_table[state][action_index] += self.alpha * (
                reward + self.gamma * max_future_q - self.q_table[state][action_index]
            )
        self.states.clear()

