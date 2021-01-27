from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from game.board import Board

BoardType = TypeVar('BoardType', bound='Board')


class MinimaxStrategy(ABC, Generic[BoardType]):

    @abstractmethod
    def get_score(self, board: BoardType, player_id, opponent_id) -> int:
        pass
