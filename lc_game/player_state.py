import bisect

from lc_game.card import Card
from lc_game.constants import NUMBER_OF_SUITS, HAND_SIZE
from lc_game.lc_action import LcAction
from lc_game.rules_error import RulesError


class PlayerState:
    def __init__(self, player_number):
        self.player_number = player_number
        self.played_cards = [[] for _ in range(NUMBER_OF_SUITS)]
        self.hand = []

    def play_card(self, card):
        if card not in self.hand:
            raise ValueError("Card doesn't exist in hand: {}".format(Card.print(card)))

        rank = Card.rank(card)
        suit = Card.suit(card)

        suit_col = self.played_cards[suit]
        if suit_col and Card.rank(suit_col[-1]) >= rank:
            raise RulesError("Card [{}] can't be played because a card of greater rank has already been played.")

        self.hand.remove(card)
        suit_col.append(card)

    def add_to_hand(self, card):
        bisect.insort(self.hand, card)

    def take_from_played(self, suit):
        if self.played_cards[suit]:
            return self.played_cards[suit].pop()
        else:
            return None

    def take_from_hand(self, card):
        if card not in self.hand:
            raise RuntimeError("Expected card [{}] to be in hand.".format(Card.format(card)))
        self.hand.remove(card)

    def deal_hand(self, deck):
        for _ in range(HAND_SIZE):
            self.add_to_hand(deck.pop())

    def score(self):
        score = 0
        for suit in range(NUMBER_OF_SUITS):
            score += self.score_suit(suit)
        return score

    def score_suit(self, suit):
        return PlayerState._score_cards(self.played_cards[suit])

    @staticmethod
    def _score_cards(cards):
        num_bets = cards.count(Card.BET_CARD)
        return (-20 + sum(cards)) * (num_bets + 1)

    def is_valid_action(self, action):
        if action.action != LcAction.PLAY_CARD:
            raise RulesError("PlayerState can only play cards.")

        card = action.card
        rank = Card.rank(card)
        suit = Card.suit(card)
        suit_col = self.played_cards[suit]
        current_rank_of_suit = Card.rank(suit_col[-1]) if suit_col else None
        return current_rank_of_suit is None or current_rank_of_suit < rank
