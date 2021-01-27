from game.player import Player
from game.players.minimax.minimax import Minimax
from game.players.minimax.minimax_strategy import MinimaxStrategy


class MinimaxPlayer(Player):
    def __init__(self, player_id, strategy: MinimaxStrategy):
        super().__init__(player_id)
        self.strategy = strategy

    def move(self, game):
        return Minimax(game, self.strategy, 3).get_action()
