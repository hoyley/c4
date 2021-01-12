from abc import abstractmethod


class Player:
    def __init__(self, player_id, _config=None):
        self.player_id = player_id

    @abstractmethod
    def move(self, game):
        pass

    @abstractmethod
    def game_over(self, game):
        pass
