import math

from lc_game.constants import NUMBER_OF_SUITS, CARDS_IN_SUIT


class Card:
    BET_CARD = 0
    RED_SUIT = 0
    GREEN_SUIT = 1
    WHITE_SUIT = 2
    BLUE_SUIT = 3
    YELLOW_SUIT = 4

    SUITS = {
        0: "Red",
        1: "Green",
        2: "White",
        3: "Blue",
        4: "Yellow"
    }

    @staticmethod
    def suit(card_number):
        return math.floor(card_number / CARDS_IN_SUIT)

    @staticmethod
    def suit_name(card_number):
        return Card.SUITS[Card.suit(card_number)]

    @staticmethod
    def rank(card_number):
        card_val = card_number % CARDS_IN_SUIT

        return Card.BET_CARD if card_val == Card.BET_CARD else card_val + 1

    @staticmethod
    def is_bet_card(card_number):
        return card_number % NUMBER_OF_SUITS == Card.BET_CARD

    @staticmethod
    def format(card_number):
        rank = Card.rank(card_number)
        suit = Card.suit_name(card_number)

        if rank == Card.is_bet_card(card_number):
            return "{}[Bet]".format(suit)
        else:
            return "{}[{}]".format(suit, rank)
