from abc import abstractmethod
import math

class Player:
    def __init__(self, player_id, config=None):
        self.player_id = player_id
        self.load_model = config["load_model"] if config else False
        self.save_frequency = config["store_freq"] if config and config["store_freq"] else math.inf
        self.games_played = 0

    @abstractmethod
    def move(self, game):
        pass

    def game_over(self, game):
        self._on_game_over(game)

        self.games_played += 1
        if self.games_played % self.save_frequency == 0:
            self.save_state()

    def _on_game_over(self, game):
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass
