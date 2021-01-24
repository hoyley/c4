from __future__ import annotations

from game.action import Action


class C4Action(Action):
    def __init__(self, player_id: int, col: int):
        super().__init__(player_id)
        self.col = col

    def _eq(self, action: C4Action) -> bool:
        return self.col == action.col

    def _hash(self) -> int:
        return hash("{}{}".format(self.player_id, self.col))
