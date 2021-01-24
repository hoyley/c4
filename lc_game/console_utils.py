from lc_game.lc_board import LcBoard
from lc_game.card import Card
from lc_game.constants import NUMBER_OF_SUITS


class ConsoleUtils:
    COL_WIDTH = 10

    @staticmethod
    def print_board(board):
        player = board.get_current_player()
        ConsoleUtils.print_board_from_perspective(board, player)

    @staticmethod
    def print_board_from_perspective(board, player_id):
        print("-----------------------------------------------------------")
        player_state = board.get_player_state(player_id)
        opponent_state = board.get_player_state(board.get_idle_player())
        print()
        ConsoleUtils.print_player_state(opponent_state, is_reversed=True)
        print()
        ConsoleUtils.print_discard(board)
        print()
        ConsoleUtils.print_player_state(player_state)
        print()
        ConsoleUtils.print_hand(player_state)

    @staticmethod
    def print_player_state(player_state, is_reversed=False):
        max_depth = len(max(player_state.played_cards, key=lambda cards: len(cards)))
        target_range = reversed(range(max_depth)) if is_reversed else range(max_depth)

        for depth in target_range:
            for suit in range(NUMBER_OF_SUITS):
                suit_cards = player_state.played_cards[suit]
                if len(suit_cards) > depth:
                    card_text = Card.rank(suit_cards[depth])
                    ConsoleUtils.print_col(card_text)
                else:
                    ConsoleUtils.print_col()
            print()

    @staticmethod
    def print_hand(player_state):
        for card in player_state.hand:
            print(Card.format(card))

    @staticmethod
    def print_discard(board):
        for suit in range(NUMBER_OF_SUITS):
            card = board.get_discard_for_suit(suit)
            if card is None:
                ConsoleUtils.print_col(Card.SUITS[suit])
            else:
                ConsoleUtils.print_col(Card.format(card))

    @staticmethod
    def print_col(text=''):
        print(ConsoleUtils.format_col(text), end='')

    @staticmethod
    def format_col(text):
        return ConsoleUtils.format_width(text, ConsoleUtils.COL_WIDTH)

    @staticmethod
    def format_width(text, width):
        format_string = '{{:>{}}}'.format(width)
        return format_string.format(text)
