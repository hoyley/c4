from typing import List

from game.action import Action
from game.player import Player
from game.two_player_turn_based_game import TwoPlayerTurnBasedGame
from lc_game.constants import PLAYER_1
from lc_game.lc_board import LcBoard


class LcGame(TwoPlayerTurnBasedGame):

    def __init__(self, board: LcBoard, player1: Player, player2: Player, is_training: bool):
        super().__init__(board, player1, player2, is_training)
        self.lc_board = board

    def get_current_player(self):
        return self.player1 if self.board.get_current_player() == PLAYER_1 else self.player2

    def _get_winner(self):
        p1_score = self.board.player_1_state.score()
        p2_score = self.board.player_2_state.score()

        return None if p1_score == p2_score else self.player1 if p1_score > p2_score else self.player2

    def get_valid_actions(self) -> List[Action]:
        return self.lc_board.get_valid_actions()
