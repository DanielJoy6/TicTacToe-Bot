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
        self.canon_cache = {}  # Cache canonical transformations for speed

    def canonical(self, board):
        """
        Convert a board into its canonical representation by considering all rotations
        and flips, and selecting the lexicographically smallest one.
        """
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

    def makeMove(self, board):
        # Find valid moves
        validMoves = [x for x in range(len(board)) if board[x] == " "]

        # Human-controlled player
        if self.strategy == "human":
            print("Your valid moves are:", validMoves)
            move = int(input("Where would you like to move? "))
            return move

        # Random player
        elif self.strategy == "random":
            return random.choice(validMoves)

        # Q-learning AI player
        elif self.strategy == "AI":
            # Use canonical board state for Q-table key
            state = self.canonical(board)

            if state not in self.q_table:
                self.q_table[state] = [0.0 for _ in range(9)]

            # Mask out illegal moves by setting their Q-values to -∞
            masked_q_values = np.array([
                self.q_table[state][i] if i in validMoves else -np.inf
                for i in range(9)
            ])

            # ε-greedy action selection
            if random.random() < self.epsilon:
                move = random.choice(validMoves)
            else:
                move = int(np.argmax(masked_q_values))

            self.states.append((state, move))
            return move

    def update_q_table(self, reward):
        """
        Update Q-values for all visited states and actions in the episode.
        Uses canonical states for both learning and prediction.
        """
        for (state, action_index) in self.states:
            # Next state's canonical Q-values aren't tracked since we're doing terminal rewards only
            max_future_q = max(self.q_table[state])
            self.q_table[state][action_index] += self.alpha * (
                reward + self.gamma * max_future_q - self.q_table[state][action_index]
            )
        self.states.clear()
