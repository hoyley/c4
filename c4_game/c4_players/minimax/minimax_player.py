from c4_game.c4_players.minimax.minimax import Minimax
from game.player import Player


class MinimaxPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def move(self, game):
        return Minimax(game, 3).get_move()
