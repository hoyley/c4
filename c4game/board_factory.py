from c4game.board import Board


class BoardFactory:
    def __init__(self, num_rows=6, num_cols=7, line_length=4):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.line_length = line_length

    def create(self):
        return Board(self.num_rows, self.num_cols, self.line_length)
