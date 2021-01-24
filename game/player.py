from abc import abstractmethod
import math

from typing import Dict

from game.action import Action


class Player:
    def __init__(self, player_id: int, config: Dict = None):
        self.player_id = player_id
        self._load_model: bool = config["load_model"] if config else False
        self._save_frequency: int = config["store_freq"] if config and config["store_freq"] else math.inf
        self._games_played = 0

    @abstractmethod
    def move(self, game) -> Action:
        pass

    def game_over(self, game):
        self._on_game_over(game)

        self._games_played += 1
        if self._games_played % self._save_frequency == 0:
            self.save_state()

    def _on_game_over(self, game):
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass
