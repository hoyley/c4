from c4players.random_player import RandomPlayer
from c4players.mcts.mcts_player import MctsPlayer
from c4players.minimax.minimax_player import MinimaxPlayer
from c4players.split_player import SplitPlayer
from c4players.human_player import HumanPlayer

class PlayerFactory:
    @staticmethod
    def create(strategy_name, player_id, config=None):
        if strategy_name == 'random':
            return RandomPlayer(player_id)
        elif strategy_name == 'mcts':
            return MctsPlayer(player_id)
        elif strategy_name == 'dqn':
            from c4players.dqn.dqn_player import DqnPlayer
            return DqnPlayer(player_id, config)
        elif strategy_name == 'minimax':
            return MinimaxPlayer(player_id)
        elif strategy_name == 'human':
            return HumanPlayer(player_id)
        elif ',' in strategy_name:
            strategies = strategy_name.split(',')
            if len(strategies) != 2:
                raise ValueError('Only two player types can be specified: {}'.format(strategy_name))

            trainer = PlayerFactory.create(strategies[0], player_id)
            player = PlayerFactory.create(strategies[1], player_id)
            return SplitPlayer(player_id, trainer, player)
        else:
            raise ValueError('No player strategy named [{}] available.', strategy_name)
