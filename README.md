# Q-Learning Tic-Tac-Toe Bot

This project implements **Q-learning reinforcement learning** to play Tic-Tac-Toe against itself to learn optimal strategies.

## Features
- Q-Learning table mapping states & actions with rewards  
- Self-play training of 100k+ rounds  
- Evaluation & training functions
- 50% reduced training time due to canonicalization of game states

## How It Works
- Board is represented as a tuple  
- Each unique state is an entry in the Q-table  
- Uses **epsilon-greedy exploration**, with epsilon decaying throughout training  

## Installation & Training

```bash
# Clone the repository
git clone https://github.com/DanielJoy6/TicTacToe-Bot.git
cd TicTacToe-Bot

# Install dependencies
pip install numpy

# Train the agent
python train.py
```

Future Improvements:
* Reducing number of boards in Q-table by mapping rotations into single state
* Saving & Loading q-table
* MatPlotLib plots of winrate over time throughout training

For any questions, please email me at danieljoy2345@gmail.com
