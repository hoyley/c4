from c4game.player import Player
from c4players.minimax.minimax import Minimax


class MinimaxPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def move(self, game):
        return Minimax(game, 3).get_move()

    def game_over(self, game):
        pass
