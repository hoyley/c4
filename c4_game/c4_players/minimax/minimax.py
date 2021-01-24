import numpy as np # type: ignore
import random

from c4_game.c4_action import C4Action
from c4_game.c4_game import C4Game
from c4_game.c4_players.minimax.window_heuristic import WindowHeuristic


class Minimax:

    # If enabled, all child operations are performed on copies of the board.
    # Array copies can be expensive when done excessively, so performance is improved if disabled.
    # If there is any threading, this should be True.
    COPY_BOARD = False
    ALPHA_BETA = True

    def __init__(self, game: C4Game, num_steps_lookahead):
        self.rows = game.board.rows
        self.cols = game.board.cols
        self.line_length = game.board.line_length
        self.player_id = game.get_current_player().player_id
        self.opponent_id = game.get_opponent(game.get_current_player).player_id
        self.starting_board = game.board.copy() if Minimax.COPY_BOARD else game.board
        self.num_steps_lookahead = num_steps_lookahead
        self.heuristic = WindowHeuristic(self.player_id, self.opponent_id)

    def get_move(self):
        allowed_moves = self.starting_board.get_valid_cols()

        move_score_dict = {}
        max_score = -np.inf
        for allowed_move in allowed_moves:
            board_after_move = Minimax.drop_piece(self.starting_board, allowed_move, self.player_id)
            minimax_score = self.minimax(board_after_move, self.num_steps_lookahead - 1, False, -np.Inf, np.Inf)
            move_score_dict[allowed_move] = minimax_score
            max_score = minimax_score if minimax_score > max_score else max_score
            Minimax.clean_up_move(board_after_move)

        moves_with_max_score = [move for move in move_score_dict if move_score_dict[move] == max_score]

        return C4Action(self.player_id, random.choice(moves_with_max_score))

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        available_moves = board.get_valid_cols()

        if depth == 0 or not available_moves or board.check_win_from_last_move():
            return self.get_score(board)

        if maximizing_player:
            max_eval = -np.Inf
            for col in available_moves:
                board_after_move = Minimax.drop_piece(board, col, self.player_id)
                max_eval = max(max_eval, self.minimax(board_after_move, depth - 1, False, alpha, beta))
                Minimax.clean_up_move(board_after_move)

                alpha = max(alpha, max_eval)
                if Minimax.ALPHA_BETA and alpha > beta:
                    break
            return max_eval
        else:
            min_eval = np.Inf
            for col in available_moves:
                board_after_move = Minimax.drop_piece(board, col, self.opponent_id)
                min_eval = min(min_eval, self.minimax(board_after_move, depth - 1, True, alpha, beta))
                Minimax.clean_up_move(board_after_move)

                beta = min(beta, min_eval)
                if Minimax.ALPHA_BETA and beta <= alpha:
                    break
            return min_eval

    def get_score(self, board):
        return self.heuristic.score_board(board)

    @staticmethod
    def is_terminal_node(board):
        return not board.get_valid_moves()

    @staticmethod
    def drop_piece(board, col, player_id):
        next_board = board.copy() if Minimax.COPY_BOARD else board
        next_board.play(C4Action(player_id, col))
        return next_board

    @staticmethod
    def clean_up_move(board):
        if not Minimax.COPY_BOARD:
            board.undo_move()

    @staticmethod
    def check_window(window, num_discs, piece, config):
        return window.count(piece) == num_discs and window.count(0) == config.line_length - num_discs
