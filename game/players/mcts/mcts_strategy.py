from abc import abstractmethod
from typing import List, Tuple

from game.action import Action
from game.board import Board
from game.two_player_turn_based_game import TwoPlayerTurnBasedGame


class MctsStrategy:

    @abstractmethod
    def get_opponent_moves_to_advance(self, board: Board) -> List[Action]:
        self

    @abstractmethod
    def get_scores(self, game: TwoPlayerTurnBasedGame) -> Tuple[int, int]:
        pass
