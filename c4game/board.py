import copy
from collections import deque

class Board:
    PLAYER_1_TOKEN, PLAYER_2_TOKEN, EMPTY_TOKEN = 1, -1, 0

    def __init__(self, rows, cols, line_length):
        self.rows = rows
        self.cols = cols
        self.line_length = line_length
        self.board = [0] * self.rows * self.cols
        self.col_counts = [0 for _ in range(self.cols)]
        self.last_played = []

    def play(self, col, player_value):
        if 0 > col >= self.cols:
            raise ValueError('Column {} is out of bounds [0,{}].'.format(col, self.cols - 1))

        if player_value != Board.PLAYER_1_TOKEN and player_value != Board.PLAYER_2_TOKEN:
            raise ValueError('player_value is not in acceptable values [{},{}].'
                             .format(Board.PLAYER_2_TOKEN, Board.PLAYER_2_TOKEN))

        if self.col_counts[col] >= self.rows:
            raise ValueError('Column {} is already full.'.format(col))

        self.set(self.col_counts[col], col, player_value)
        self.col_counts[col] += 1
        self.last_played.append(col)

    def get(self, row, col):
        return self.board[row * self.cols + col]

    def set(self, row, col, value):
        self.board[row * self.cols + col] = value

    def get_valid_moves(self):
        return [c for c, count in enumerate(self.col_counts) if count < self.rows]

    def copy(self):
        return copy.deepcopy(self)

    def undo_move(self):
        last_played = self.last_played.pop()

        if last_played:
            self.col_counts[last_played] -= 1
            self.set(self.col_counts[last_played], last_played, Board.EMPTY_TOKEN)

    def last_column_played(self):
        return self.last_played[-1] if self.last_played else None

    def check_win_from_last_move(self):
        if not self.last_column_played():
            return False

        start_col = self.last_column_played()
        start_row = self.col_counts[start_col] - 1
        player_val = self.get(start_row, start_col)

        for c in range(-1, 1):
            for r in range(-1, 1):
                if [c, r] != [0, 0] and \
                        self._check_win_in_direction(player_val, [start_row, start_col], [r, c], self.line_length - 1):
                    return True

    def print(self):
        print('\n'.join([''.join(['{:4}'.format(self.get(row, col)) for col in range(self.cols)])
                         for row in reversed(range(self.rows))]))

    def _check_win_in_direction(self, player_val, from_location, direction, remaining):
        if remaining == 0:
            return True

        new_row = from_location[0] + direction[0]
        new_col = from_location[1] + direction[1]

        return 0 <= new_col < self.cols and 0 <= new_row < self.rows and self.get(new_row, new_col) == player_val \
            and self._check_win_in_direction(player_val, [new_row, new_col], direction, remaining - 1)
