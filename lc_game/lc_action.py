from __future__ import annotations
from game.action import Action
from lc_game.card import Card


class LcAction(Action):
    PLAY_CARD = 0
    DISCARD_CARD = 1
    DRAW_CARD = 2
    STEAL_CARD = 3

    def __init__(self, player_id: int, action, card=None):
        super().__init__(player_id)
        self.action = action
        self.card = card

    def is_give_card(self):
        return self.action == LcAction.PLAY_CARD or self.action == LcAction.DISCARD_CARD

    def is_take_card(self):
        return not self.is_give_card()

    def format(self):
        if self.action == LcAction.DRAW_CARD:
            return "Draw Card"
        elif self.action == LcAction.STEAL_CARD:
            return "Steal {}".format(Card.format(self.card))
        elif self.action == LcAction.DISCARD_CARD:
            return "Discard {}".format(Card.format(self.card))
        elif self.action == LcAction.PLAY_CARD:
            return "Play {}".format(Card.format(self.card))

    def _eq(self, other: LcAction) -> bool:
        return self.action == other.action and self.player_id == other.player_id \
               and self.card == other.card

    def _hash(self) -> int:
        card_val = 0 if self.card is None else self.card + 1
        return self.player_id << 31 ^ self.action << 29 ^ card_val

