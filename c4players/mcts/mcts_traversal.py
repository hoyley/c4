from c4game.player import Player
from c4players.mcts.node import Node
import math


class MctsTraversal:

    def __init__(self, root, player, opponent, is_training):
        self.current_node = root
        self.player = player
        self.opponent = opponent
        self.is_training = is_training

    def move(self, board):
        self._update_opponents_move(board)
        self._add_child_nodes_if_necessary(board)

        best_move_node = self.current_node.highest_ucb_child() \
            if self.is_training \
            else self.current_node.best_score_child()

        self._set_next_node(best_move_node)

        return self.current_node.col

    def end_game(self, game):
        current_player_id = game.current_player.player_id
        winner_id = game.winner.player_id if game.winner else None
        board = game.board

        if current_player_id != self.current_node.player_id:
            self._update_opponents_move(board)

        win = winner_id == self.current_node.player_id
        draw = winner_id is None
        score = 1 if win else 0 if draw else -1
        opponent_score = score * -1
        self.current_node.update_score(score, opponent_score)

    def _update_opponents_move(self, board):
        last_column_played = board.last_column_played()
        if board.last_column_played() is not None:
            matching_nodes = filter(lambda node: node.col == last_column_played, self.current_node.children)
            opponent_node = next(matching_nodes, None)
            if opponent_node is None:
                opponent_node = self.current_node.add_child(self.opponent.player_id, last_column_played)

            self._set_next_node(opponent_node)

    def _set_next_node(self, node):
        self.current_node = node

    def _add_child_nodes_if_necessary(self, board):
        if self.current_node.is_leaf():
            for move in board.get_valid_moves():
                self.current_node.add_child(self.player.player_id, move)
