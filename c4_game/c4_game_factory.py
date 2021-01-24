from c4_game.c4_board import C4Board
from c4_game.c4_game import C4Game
from game.game_factory import GameFactory
from game.player import Player
from game.two_player_turn_based_game import TwoPlayerTurnBasedGame


class C4GameFactory(GameFactory):
    def __init__(self, player1: Player, player2: Player, num_rows: int = 6, num_cols: int = 7, line_length: int = 4):
        super().__init__(player1, player2)
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.line_length = line_length

    def create_game(self, is_training: bool) -> TwoPlayerTurnBasedGame:
        return C4Game(self._create_board(), self._player1, self._player2, is_training)

    def _create_board(self) -> C4Board:
        return C4Board(self.num_rows, self.num_cols, self.line_length)

