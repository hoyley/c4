from c4players.random_player import RandomPlayer


class PlayerFactory:
    @staticmethod
    def create(strategy_name, args=None):
        if strategy_name == 'random':
            return RandomPlayer(**args)
        else:
            raise ValueError('No player strategy named [{}] available.', strategy_name)
