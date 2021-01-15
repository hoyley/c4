from c4game.player import Player
import random


class RandomPlayer(Player):

    def move(self, game):
        return random.choice(game.board.get_valid_moves())

