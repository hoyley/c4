# C4 : Reinforcement Learning Approaches for Games

An exploratory project to learn and implement Reinforcement Learning approaches to solve simple games. 
Initial approaches to RL will include Monte Carlo Tree Search (MCTS) and Deep Q-Networks (DQN).
Other non-RL approaches including Convolutional Neural Networks (CNN) will be considered. 

| Game          | Approach                          | Status        |
| :---          | :---                              | :---          |
| Connect 4     | Monte Carlo Tree Search(MTCS)     | Implemented   |
| Connect 4     | Deep Q-Network (DQN)              | Pending       |


Much of the inspiration for the Connect4 approach comes from [this article](https://codebox.net/pages/connect4). 
If any articles are used in the making of this project, all intent is to understand and implement concepts,
rather than copy code.

## Running the Project

### Prerequisites 

- Python 3

### Tests
To execute test, run:
```bash
python3 test_c4.py
```

### Execution

To train and run MTCS on the Connect4 game, run the following command.
```bash
python3 runner.py --p1strategy random --p2strategy mcts --numTraining 500000 --numGames 1000 
```
This command will run 500,000 training simulations with player 1 using random strategy and player 2 using MCTS. 
Following training, 1,000 simulations will be run.

Use `python3 runner.py --help` for more detailed instructions. Todo: Implement more detailed instructions :)
