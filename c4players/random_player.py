from c4game.player import Player
import random


class RandomPlayer(Player):

    def move(self, board):
        return random.choice(board.get_valid_moves())


