"""Player that employs a basic Deep Q-Learning agent"""
import random
import numpy as np
from collections import deque
from base_player import Player

from keras import models, layers, optimizers

class DQNPlayer(Player):
    """
    Deep Q-Learning Player
    - Uses a small neural network to approximate Q(s,a)
    """

    def __init__(self, name, symbol, lr=0.001, gamma=0.99, epsilon=1.0,
                 epsilon_min=0.05, epsilon_decay=0.999):
        super().__init__(name)
        self.symbol = symbol
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.memory = deque(maxlen=50000)

        self.model = self._build_model()

    def _build_model(self):
        """Create a small NN: input=board(9), output=Q-value per move(9)."""
        if models is None:
            return None

        model = models.Sequential([
            layers.Input(shape=(9,)),
            layers.Dense(64, activation="relu"),
            layers.Dense(64, activation="relu"),
            layers.Dense(9, activation="linear")
        ])
        model.compile(optimizer=optimizers.Adam(self.lr), loss="mse")
        return model

    def makeMove(self, board, gametype):
        """Choose a move using epsilon-greedy policy."""
        valid_moves = [i for i in range(len(board)) if board[i] == 0]

        # Random exploration
        if random.random() < self.epsilon:
            return random.choice(valid_moves)

        # Model inference
        state = np.array(board, dtype=np.float32)
        q_values = self.model.predict(state.reshape(1, -1), verbose=0)[0]

        # Mask illegal moves
        masked = [(q_values[i] if i in valid_moves else -9999) for i in range(len(board))]

        return int(np.argmax(masked))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size=64):
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_qs = self.model.predict(next_state.reshape(1, -1), verbose=0)[0]
                target = reward + self.gamma * np.max(next_qs)

            q_values = self.model.predict(state.reshape(1, -1), verbose=0)
            q_values[0][action] = target
            self.model.fit(state.reshape(1, -1), q_values, epochs=1, verbose=0)

        # Decay exploration
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def reset(self):
        pass
