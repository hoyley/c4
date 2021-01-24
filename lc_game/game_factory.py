from game.game_factory import GameFactory
from lc_game.lc_board import LcBoard
from lc_game.lc_game import LcGame


class LcGameFactory(GameFactory):

    def create_game(self, is_training):
        return LcGame(self._create_board(), self._player1, self._player2, is_training)

    def _create_board(self) -> LcBoard:
        return LcBoard()
