import numpy
class Player:
    def __init__(self, name, strategy, epsilon):
        self.name = name
        self.strategy = strategy
        self.epsilon = epsilon
        self.q_table = {}
        self.states = []
    def makeMove(self, board):
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
            state = tuple(board)
            move_index = 0
            if state not in self.q_table:
                self.q_table[state] = [0.0 for _ in range(9)]
            valid_q_values = [self.q_table[state][i] if i in validMoves else -np.inf for i in range(9)]
            move_index = np.argmax(valid_q_values)

            if(random.random() < self.epsilon):
                move_index = random.randint(0, len(validMoves)-1)
                move = validMoves[move_index]
            else:
                print("validMoves:", validMoves)
                move_index = np.argmax(self.q_table[state])
                print("qtable state:", self.q_table[state])
                print("move_index:", move_index)
                move = validMoves[move_index]
            self.states.append((state, move_index))
            return move
    '''
    def updateQTable(self, reward):
        for(state, action_index) in self.states:
            self.q_table[state][action_index] += reward
        self.states.clear()
    '''
    #New Version
    def updateQTable(self, reward):
        alpha = 0.1  # Learning rate
        gamma = 0.9  # Discount factor
        for (state, action_index) in self.states:
            max_future_q = max(self.q_table[state])  # Max Q-value of next state
            self.q_table[state][action_index] += alpha * (reward + gamma * max_future_q - self.q_table[state][action_index])
        self.states.clear()
