# C4 : Reinforcement Learning Approaches for Games

An exploratory project to learn and implement Reinforcement Learning approaches to solve simple games. 
Initial approaches to RL will include Monte Carlo Tree Search (MCTS) and Deep Q-Networks (DQN).
Other non-RL approaches including Convolutional Neural Networks (CNN) will be considered. 

| Game          | Approach                          | Status        | Command Line Name |  
| :---          | :---                              | :---          | :---              |
| Connect 4     | Random                            | Implemented   | random            |
| Connect 4     | Minimax                           | Implemented   | minimax           |
| Connect 4     | Monte Carlo Tree Search(MTCS)     | Implemented   | mcts              |
| Connect 4     | Deep Q-Network (DQN)              | Implemented   | dqn               |

Much of the inspiration for the Connect4 approach comes from [this article](https://codebox.net/pages/connect4). 
If any articles are used in the making of this project, all intent is to understand and implement concepts,
rather than copy code.

## Running the Project

### Prerequisites 

- Python3
- Anaconda

### Setup
```bash
conda env create
conda activate c4
```

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

### Alternate Docker Setup

On a Mac or PC running an Intel CPU and no discrete graphics, I've seen approximately a 20% increase in speed of 
DQN training using pre-built GCP docker images. This depends on your processor architecture and may not work for all 
configurations.

```
docker run -it --rm -v $(pwd):/c4 gcr.io/deeplearning-platform-release/tf2-cpu.2-0 python3 /c4/runner.py --p1strategy dqn --p2strategy mcts --numTraining 50 --numGames 10 -v
```
OR
```
./bin/docker-cpu-runner.sh --p1strategy dqn --p2strategy mcts --numTraining 50 --numGames 10 -v
```
