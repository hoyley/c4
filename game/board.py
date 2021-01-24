from __future__ import annotations
import copy
from abc import abstractmethod, ABC
from typing import ClassVar, List, Optional, Generic, TypeVar

from game.action import Action

ActionType = TypeVar('ActionType', bound='Action')


class Board(ABC, Generic[ActionType]):
    _last_action: ClassVar[List[ActionType]]

    def __init__(self):
        self._last_action = []

    def play(self, action: ActionType):
        self._last_action.append(action)

    @abstractmethod
    def is_game_over(self) -> bool:
        pass

    @abstractmethod
    def undo_move(self):
        pass

    def get_last_action(self) -> Optional[Action]:
        return self._last_action[-1] if self._last_action else None

    def copy(self) -> Board:
        return copy.deepcopy(self)
