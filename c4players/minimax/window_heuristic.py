

class WindowHeuristic:

    NORTH = [1, 0]
    EAST = [0, 1]
    NORTH_EAST = [1, 1]
    SOUTH_EAST = [-1, 1]

    def __init__(self, player_id, opponent_id):
        self.player_id = player_id
        self.opponent_id = opponent_id

    def score_board(self, board):
        window_counts = WindowHeuristic.WindowCounts()

        # Count in horizontal orientation
        for row in range(board.rows):
            for col in range(board.cols - (board.line_length - 1)):
                self.count_window_contents(board, row, col, WindowHeuristic.EAST, window_counts)
        # Count in vertical orientation
        for row in range(board.rows - (board.line_length - 1)):
            for col in range(board.cols):
                self.count_window_contents(board, row, col, WindowHeuristic.NORTH, window_counts)
        # Count in positive diagonal
        for row in range(board.rows - (board.line_length - 1)):
            for col in range(board.cols - (board.line_length - 1)):
                self.count_window_contents(board, row, col, WindowHeuristic.NORTH_EAST, window_counts)
        # Count in negative diagonal
        for row in range(board.line_length - 1, board.rows):
            for col in range(board.cols - (board.line_length - 1)):
                self.count_window_contents(board, row, col, WindowHeuristic.SOUTH_EAST, window_counts)

        return window_counts.get_score()

    def count_window_contents(self, board, start_row, start_col, direction, window_counts):
        num_player = 0
        num_opponent = 0
        num_empty = 0
        cur_row = start_row
        cur_col = start_col
        direction_row = direction[0]
        direction_col = direction[1]

        for _ in range(board.line_length):
            if not (0 <= cur_row < board.rows and 0 <= cur_col < board.cols):
                break

            val = board.get(cur_row, cur_col)
            if val == self.player_id:
                num_player += 1
            elif val == self.opponent_id:
                num_opponent += 1
            else:
                num_empty += 1

            cur_row = cur_row + direction_row
            cur_col = cur_col + direction_col

        if num_player >= 3:
            window_counts.num_threes += 1
        if num_player == 4:
            window_counts.num_fours += 1
        if num_opponent >= 3:
            window_counts.num_threes_opp += 1
        if num_opponent == 4:
            window_counts.num_fours_opp += 1

    class WindowCounts:
        def __init__(self):
            self.num_threes = 0
            self.num_fours = 0
            self.num_threes_opp = 0
            self.num_fours_opp = 0

        def get_score(self):
            return 1 * self.num_threes \
                   + 1e4 * self.num_fours \
                   - 1 * self.num_threes_opp \
                   - 1e4 * self.num_fours_opp
