from abc import ABC, abstractmethod
from typing import TypeVar

ActionImpl = TypeVar('ActionImpl', bound='Action')


class Action(ABC):

    def __init__(self, player_id: int):
        self.player_id = player_id

    def __eq__(self, other):
        return type(self) == type(other) and self.player_id == other.player_id and self._eq(other)

    def __hash__(self):
        return self._hash()

    @abstractmethod
    def _eq(self: ActionImpl, action: ActionImpl) -> bool:
        return False

    @abstractmethod
    def _hash(self) -> int:
        return 0
