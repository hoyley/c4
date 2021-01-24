from abc import abstractmethod

from game.player import Player
from game.two_player_turn_based_game import TwoPlayerTurnBasedGame


class GameFactory:
    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2

    @abstractmethod
    def create_game(self, is_training: bool) -> TwoPlayerTurnBasedGame:
        pass
