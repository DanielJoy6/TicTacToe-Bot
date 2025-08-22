# Q-Learning Tic-Tac-Toe Bot

This projects implements Q-learning reinforcement to play Tic-Tac-Toe against
itself to learn optimal strategies

## **Features**
* Q-Learning table to map states & actions with rewards
* Self-play training of 100k+ rounds
* Evaluation & training functions

## **How it works**
* Board is represented by a tuple
* Each unique state is an individual entry in the q-table
* Uses epsilon-greedy exploration, then decays epsilon throughout training
* Q-Table updates using:

 \[
   Q(s,a) \leftarrow Q(s,a) + \alpha \Big[ r + \gamma \cdot \max_{a'} Q(s', a') - Q(s,a) \Big]
   \]

  How to install/train:
  1. Clone the repository:
git clone https://github.com/DanielJoy6/TicTacToe-Bot.git
cd TicTacToe-Bot
  2. Install numpy
  3. Train agent with train.py
     * it will automatically create games and train 2 agents against each other. You're welcome to add more!
     
  Future Improvements:
  * Reducing number of boards in Q-table by mapping rotations into single state
  * Saving & Loading q-table
  * MatPlotLib plots of winrate over time throughout training
