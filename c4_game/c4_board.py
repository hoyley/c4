from typing import List

from c4_game.c4_action import C4Action
from game.action import Action
from game.board import Board


class C4Board(Board[C4Action]):
    PLAYER_1_TOKEN, PLAYER_2_TOKEN, EMPTY_TOKEN = 1, -1, 0

    def __init__(self, rows: int, cols: int, line_length: int):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.line_length = line_length
        self.board = [0] * self.rows * self.cols
        self.col_counts = [0] * self.cols

    def play(self, action: C4Action):
        col = action.col
        player_value = action.player_id

        if 0 > col >= self.cols:
            raise ValueError('Column {} is out of bounds [0,{}].'.format(col, self.cols - 1))

        if player_value != C4Board.PLAYER_1_TOKEN and player_value != C4Board.PLAYER_2_TOKEN:
            raise ValueError('player_value is not in acceptable values [{},{}].'
                             .format(C4Board.PLAYER_2_TOKEN, C4Board.PLAYER_2_TOKEN))

        if self.col_counts[col] >= self.rows:
            raise ValueError('Column {} is already full.'.format(col))

        self.set(self.col_counts[col], col, player_value)
        self.col_counts[col] += 1

        super().play(action)

    def is_game_over(self) -> bool:
        return not self.get_valid_cols() or self.check_win_from_last_move()

    def get_valid_cols(self) -> List[int]:
        return [c for c, count in enumerate(self.col_counts) if count < self.rows]

    def get_valid_actions(self) -> List[Action]:
        player_id = self.get_current_player_id()
        return [C4Action(player_id, c) for c, count in enumerate(self.col_counts) if count < self.rows]

    def get(self, row, col):
        return self.board[row * self.cols + col]

    def set(self, row, col, value):
        self.board[row * self.cols + col] = value

    def undo_action(self):
        last_played = self._last_action.pop()

        if last_played is not None:
            self.col_counts[last_played.col] -= 1
            self.set(self.col_counts[last_played.col], last_played.col, C4Board.EMPTY_TOKEN)

    def check_win_from_last_move(self):
        last_played = self.get_last_action().col

        start_col = last_played
        start_row = self.col_counts[start_col] - 1
        player_val = self.get(start_row, start_col)
        start_location = [start_row, start_col]

        return self._count_vertical(player_val, start_location) >= self.line_length or \
               self._count_horizontal(player_val, start_location) >= self.line_length or \
               self._count_positive_diagonal(player_val, start_location) >= self.line_length or \
               self._count_negative_horizontal(player_val, start_location) >= self.line_length

    def get_current_player_id(self):
        last_action = self.get_last_action()

        return self.PLAYER_1_TOKEN if not last_action or last_action.player_id == self.PLAYER_2_TOKEN \
            else self.PLAYER_2_TOKEN

    def print(self):
        print('\n'.join([''.join(['{:>4}'.format(self.get(row, col)) for col in range(self.cols)])
                         for row in reversed(range(self.rows))]))
        print("   -" * self.cols)
        print(''.join(['{:4}'.format(col) for col in range(self.cols)]))

    def print_replace(self, player1, player2, empty):
        new_board = self.copy()
        for i in range(len(self.board)):
            new_board.board[i] = player1 if self.board[i] == C4Board.PLAYER_1_TOKEN \
                else player2 if self.board[i] == C4Board.PLAYER_2_TOKEN \
                else empty

        new_board.print()

    def _count_vertical(self, player_val, from_location):
        return 1 + self._count_in_direction(player_val, from_location, [1, 0]) \
               + self._count_in_direction(player_val, from_location, [-1, 0])

    def _count_horizontal(self, player_val, from_location):
        return 1 + self._count_in_direction(player_val, from_location, [0, 1]) \
               + self._count_in_direction(player_val, from_location, [0, -1])

    def _count_positive_diagonal(self, player_val, from_location):
        return 1 + self._count_in_direction(player_val, from_location, [1, 1]) \
               + self._count_in_direction(player_val, from_location, [-1, -1])

    def _count_negative_horizontal(self, player_val, from_location):
        return 1 + self._count_in_direction(player_val, from_location, [1, -1]) \
               + self._count_in_direction(player_val, from_location, [-1, 1])

    def _count_in_direction(self, player_val, from_location, direction):
        new_row = from_location[0] + direction[0]
        new_col = from_location[1] + direction[1]

        in_bounds = 0 <= new_col < self.cols and 0 <= new_row < self.rows

        if (not in_bounds) or self.get(new_row, new_col) != player_val:
            return 0
        else:
            return 1 + self._count_in_direction(player_val, [new_row, new_col], direction)
