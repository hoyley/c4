import random
from typing import List

from game.action import Action
from game.board import Board as GameBoard
from lc_game.card import Card
from lc_game.constants import PLAYER_1, PLAYER_2, NUMBER_OF_SUITS
from lc_game.lc_action import LcAction
from lc_game.player_state import PlayerState
from lc_game.rules_error import RulesError


class LcBoard(GameBoard[LcAction]):
    def __init__(self):
        super().__init__()
        self.player_1_state = PlayerState(PLAYER_1)
        self.player_2_state = PlayerState(PLAYER_2)
        self.discard = [[] for _ in range(NUMBER_OF_SUITS)]
        self.deck = LcBoard._shuffle_deck()
        self.player_1_state.deal_hand(self.deck)
        self.player_2_state.deal_hand(self.deck)

    def play(self, action):
        player_state = self.get_current_player_state()

        if action.action == LcAction.PLAY_CARD:
            player_state.play_card(action.card)
        elif action.action == LcAction.DISCARD_CARD:
            suit = Card.suit(action.card)
            player_state.take_from_hand(action.card)
            self.discard[suit].append(action.card)
        elif action.action == LcAction.DRAW_CARD:
            player_state.add_to_hand(self.deck.pop())
        elif action.action == LcAction.STEAL_CARD:
            suit = Card.suit(action.card)
            self.discard[suit].pop()
            player_state.add_to_hand(action.card)
        super().play(action)

    def get_valid_actions(self) -> List[Action]:
        player_id = self.get_current_player()
        player_state = self.get_current_player_state()
        last_action = self.get_last_action()
        must_give_card = last_action is None or last_action.player_id != player_id

        actions: List[Action] = []

        # The game is over if the desk is empty
        if not self.deck:
            return actions

        if must_give_card:
            for card in player_state.hand:
                play_action = LcAction(player_id, LcAction.PLAY_CARD, card)
                if player_state.is_valid_action(play_action):
                    actions.append(play_action)
            for card in player_state.hand:
                actions.append(LcAction(player_id, LcAction.DISCARD_CARD, card))
        else:
            if self.deck:
                actions.append(LcAction(player_id, LcAction.DRAW_CARD))
                for suit in range(NUMBER_OF_SUITS):
                    if self.discard[suit]:
                        actions.append(LcAction(player_id, LcAction.STEAL_CARD, self.discard[suit][-1]))
        return actions

    def is_valid_action(self, action):
        last_action = self.last_played[-1] if self.last_played else None
        player_state = self.get_current_player_state()

        must_give_card = last_action is None or last_action.player_id != self.get_current_player()

        if must_give_card and action.action == LcAction.PLAY_CARD:
            return player_state.is_valid_action(action)
        elif must_give_card and action.action == LcAction.DISCARD_CARD:
            return True
        elif not must_give_card and action.action == LcAction.DRAW_CARD:
            return len(self.deck) > 0
        elif not must_give_card and action.action == LcAction.STEAL_CARD:
            suit = Card.suit(action.card)
            discard_pile = self.discard[suit]
            return discard_pile and discard_pile[-1] == action.card
        else:
            return False

    def is_game_over(self):
        return not self.deck

    def get_current_player(self):
        last_action = self.get_last_action()
        if last_action is None:
            return self.player_1_state.player_number

        swap_player = last_action.is_take_card()

        if (swap_player and last_action.player_id == PLAYER_2) or (not swap_player and last_action.player_id == PLAYER_1):
            return PLAYER_1
        else:
            return PLAYER_2

    def get_idle_player(self):
        return (self.get_current_player() + 1) % 2

    def get_current_player_state(self):
        return self.player_1_state if self.get_current_player() == PLAYER_1 else self.player_2_state

    def get_player_state(self, player_id):
        return self.player_1_state if player_id == PLAYER_1 else self.player_2_state

    def get_discard_for_suit(self, suit):
        discard_pile = self.discard[suit]
        return discard_pile[-1] if discard_pile else None

    def get_last_opponent_actions(self):
        opponent_actions = []
        current_player_id = self.get_current_player()

        for i in reversed(range(len(self._last_action))):
            if self._last_action[i].player_id == current_player_id:
                break
            else:
                opponent_actions.append(self._last_action[i])
        return reversed(opponent_actions)

    def undo_action(self):
        last_action = self.last_played[-1] if self.last_played else None
        player_state = self.get_player_state(last_action.player_id)

        if not last_action:
            raise RulesError("Cannot undo, no moves have been played.")

        if last_action.action == LcAction.PLAY_CARD:
            suit = Card.suit(last_action.card)
            card = player_state.take_from_played(suit)
            if card != last_action.card:
                raise RuntimeError("Invalid board state during undo operation")
            player_state.add_to_hand(card)
        elif last_action.action == LcAction.DISCARD_CARD:
            suit = Card.suit(last_action.card)
            card = self.discard[suit].pop()
            if card != last_action.card:
                raise RuntimeError("Invalid board state during undo operation")
            player_state.add_to_hand(card)
        elif last_action.action == LcAction.DRAW_CARD:
            self.deck.append(last_action.card)
            player_state.add_to_hand(last_action.card)
        elif last_action.action == LcAction.STEAL_CARD:
            suit = Card.suit(last_action.card)
            self.discard[suit].append(last_action.card)
            player_state.take_from_hand(last_action.card)

    @staticmethod
    def _shuffle_deck():
        num_cards = 10*NUMBER_OF_SUITS
        return random.sample(range(num_cards), num_cards)
