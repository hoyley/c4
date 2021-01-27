from typing import List

from c4_game.c4_board import C4Board
from game.action import Action
from game.player import Player
from game.two_player_turn_based_game import TwoPlayerTurnBasedGame


class C4Game(TwoPlayerTurnBasedGame):

    def __init__(self, board: C4Board, player1: Player, player2: Player, is_training: bool):
        super().__init__(board, player1, player2, is_training)
        self.c4_board = board

    def get_current_player(self):
        current_id = self.c4_board.get_current_player_id()
        return self.player1 if self.player1.player_id == current_id else self.player2

    def get_valid_actions(self) -> List[Action]:
        return self.c4_board.get_valid_actions()

    def _get_winner(self):
        if not self.game_over:
            return None
        elif self.winner:
            return self.winner
        elif self.c4_board.check_win_from_last_move():
            return self.get_opponent(self.get_current_player())
