import random
import numpy as np
from base_player import Player

class QLPlayer(Player):
    def __init__(self, name, epsilon, alpha, gamma, symbol):
        super().__init__(name)
        self.epsilon = epsilon
        self.Q_X = {}
        self.Q_O = {}
        self.states = []
        self.alpha = alpha
        self.gamma = gamma
        self.symbol = symbol
        self.prev_state = None
        self.prev_action = None

    def get_Q(self):
        """Return the correct Q-table for this player's symbol."""
        return self.Q_X if self.symbol == 1 else self.Q_O

    def makeMove(self, board, gametype):
        # Find valid moves
        state = tuple(x * self.symbol for x in board)
        Q = self.get_Q()
        validMoves = [x for x in range(len(board)) if board[x] == 0]

        if state not in Q:
            Q[state] = [0.0] * 9
        q_values = Q[state]
        masked_q_values = np.array([
            q_values[i] if i in validMoves else -np.inf
            for i in range(9)
        ])
        # ε-greedy action selection
        if random.random() < self.epsilon:
            action = random.choice(validMoves)
        else:
            action = int(np.argmax(masked_q_values))
        if gametype == "train":
            self.prev_state = state
            self.prev_action = action
        return action

    def update_q_table(self, reward, next_board):
        """
        TD(0) update after each move:
        Q(s,a) += α ( r + γ maxQ(s') - Q(s,a) )
        """
        if self.prev_state is None:
            return

        Q = self.get_Q()
        s = self.prev_state
        a = self.prev_action

        # Future state
        s_next = tuple(x * self.symbol for x in next_board)
        if s_next not in Q:
            Q[s_next] = [0.0] * 9

        # TD target
        td_target = reward + self.gamma * max(Q[s_next])
        td_error = td_target - Q[s][a]

        # Update
        Q[s][a] += self.alpha * td_error

        # Reset stored transition
        self.prev_state = None
        self.prev_action = None

    def reset(self):
        self.prev_state = None
        self.prev_action = None