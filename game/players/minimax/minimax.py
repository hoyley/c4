import random

import numpy as np  # type: ignore

from game.players.minimax.minimax_strategy import MinimaxStrategy
from game.two_player_turn_based_game import TwoPlayerTurnBasedGame


class Minimax:

    # If enabled, all child operations are performed on copies of the board.
    # Array copies can be expensive when done excessively, so performance is improved if disabled.
    # If there is any threading, this should be True.
    COPY_BOARD = False
    ALPHA_BETA = True

    def __init__(self, game: TwoPlayerTurnBasedGame, strategy: MinimaxStrategy, num_steps_lookahead):
        self.strategy = strategy
        self.player_id = game.get_current_player().player_id
        self.opponent_id = game.get_opponent(game.get_current_player).player_id
        self.starting_board = game.board.copy() if Minimax.COPY_BOARD else game.board
        self.num_steps_lookahead = num_steps_lookahead

    def get_action(self):
        allowed_actions = self.starting_board.get_valid_actions()

        action_score_dict = {}
        max_score = -np.inf
        for allowed_action in allowed_actions:
            board_after_action = Minimax._perform_action(self.starting_board, allowed_action)
            minimax_score = self._minimax(board_after_action, self.num_steps_lookahead - 1, False, -np.Inf, np.Inf)
            action_score_dict[allowed_action] = minimax_score
            max_score = minimax_score if minimax_score > max_score else max_score
            Minimax._clean_up_action(board_after_action)

        actions_with_best_score = [action for action in action_score_dict if action_score_dict[action] == max_score]

        return random.choice(actions_with_best_score)

    def _minimax(self, board, depth, maximizing_player, alpha, beta):
        available_actions = board.get_valid_actions()

        if depth == 0 or board.is_game_over():
            return self._get_score(board) / (self.num_steps_lookahead - depth)

        if maximizing_player:
            max_eval = -np.Inf
            for action in available_actions:
                board_after_action = Minimax._perform_action(board, action)
                max_eval = max(max_eval, self._minimax(board_after_action, depth - 1, False, alpha, beta))
                Minimax._clean_up_action(board_after_action)

                alpha = max(alpha, max_eval)
                if Minimax.ALPHA_BETA and alpha > beta:
                    break
            return max_eval
        else:
            min_eval = np.Inf
            for action in available_actions:
                board_after_action = Minimax._perform_action(board, action)
                min_eval = min(min_eval, self._minimax(board_after_action, depth - 1, True, alpha, beta))
                Minimax._clean_up_action(board_after_action)

                beta = min(beta, min_eval)
                if Minimax.ALPHA_BETA and beta <= alpha:
                    break
            return min_eval

    def _get_score(self, board):
        return self.strategy.get_score(board, self.player_id, self.opponent_id)

    @staticmethod
    def _is_terminal_node(board):
        return not board.get_valid_actions()

    @staticmethod
    def _perform_action(board, action):
        next_board = board.copy() if Minimax.COPY_BOARD else board
        next_board.play(action)
        return next_board

    @staticmethod
    def _clean_up_action(board):
        if not Minimax.COPY_BOARD:
            board.undo_action()

    @staticmethod
    def _check_window(window, num_discs, piece, config):
        return window.count(piece) == num_discs and window.count(0) == config.line_length - num_discs
