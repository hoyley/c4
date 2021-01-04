from c4players.random_player import RandomPlayer
from c4players.mcts.mcts_player import MctsPlayer
from c4players.dqn.dqn_player import DqnPlayer


class PlayerFactory:
    @staticmethod
    def create(strategy_name, args=None):
        if strategy_name == 'random':
            return RandomPlayer(**args)
        elif strategy_name == 'mcts':
            return MctsPlayer(**args)
        elif strategy_name == 'dqn':
            return DqnPlayer(**args)
        else:
            raise ValueError('No player strategy named [{}] available.', strategy_name)
