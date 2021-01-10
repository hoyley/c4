import numpy as np
import random
from c4players.minimax.window_heuristic import WindowHeuristic


class Minimax:

    # If enabled, all child operations are performed on copies of the board.
    # Array copies can be expensive when done excessively, so performance is improved if disabled.
    # If there is any threading, this should be True.
    COPY_BOARD = False

    def __init__(self, game, num_steps_lookahead):
        self.rows = game.board.rows
        self.cols = game.board.cols
        self.line_length = game.board.line_length
        self.player_id = game.current_player.player_id
        self.opponent_id = game.get_opponent(game.current_player).player_id
        self.starting_board = game.board.copy() if Minimax.COPY_BOARD else game.board
        self.num_steps_lookahead = num_steps_lookahead

    def get_move(self):
        allowed_moves = self.starting_board.get_valid_moves()

        move_score_dict = {}
        max_score = -np.inf
        for allowed_move in allowed_moves:
            board_after_move = Minimax.drop_piece(self.starting_board, allowed_move, self.player_id)
            minimax_score = self.minimax(board_after_move, self.num_steps_lookahead - 1, False)
            move_score_dict[allowed_move] = minimax_score
            max_score = minimax_score if minimax_score > max_score else max_score
            Minimax.clean_up_move(board_after_move)

        moves_with_max_score = [move for move in move_score_dict if move_score_dict[move] == max_score]

        return random.choice(moves_with_max_score)

    def minimax(self, board, depth, maximizing_player):
        available_moves = board.get_valid_moves()

        if depth == 0 or not available_moves or board.check_win_from_last_move():
            return self.get_heuristic(board)

        if maximizing_player:
            max_eval = -np.Inf
            for col in available_moves:
                board_after_move = Minimax.drop_piece(board, col, self.player_id)
                max_eval = max(max_eval, self.minimax(board_after_move, depth - 1, False))
                Minimax.clean_up_move(board_after_move)
            return max_eval
        else:
            min_eval = np.Inf
            for col in available_moves:
                board_after_move = Minimax.drop_piece(board, col, self.opponent_id)
                min_eval = min(min_eval, self.minimax(board_after_move, depth - 1, True))
                Minimax.clean_up_move(board_after_move)
            return min_eval

    def get_heuristic(self, board):
        return WindowHeuristic(self.player_id, self.opponent_id).score_board(board)

    @staticmethod
    def is_terminal_node(board):
        return not board.get_valid_moves()

    @staticmethod
    def drop_piece(board, col, player_id):
        next_board = board.copy() if Minimax.COPY_BOARD else board
        next_board.play(col, player_id)
        return next_board

    @staticmethod
    def clean_up_move(board):
        if not Minimax.COPY_BOARD:
            board.undo_move()

    @staticmethod
    def check_window(window, num_discs, piece, config):
        return window.count(piece) == num_discs and window.count(0) == config.line_length - num_discs
