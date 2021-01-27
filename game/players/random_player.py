
import random
from typing import Dict

from game.player import Player


class RandomPlayer(Player):
    def __init__(self, player_id: int, config: Dict = None):
        super().__init__(player_id, config)

    def move(self, game):
        return random.choice(game.get_valid_actions())

