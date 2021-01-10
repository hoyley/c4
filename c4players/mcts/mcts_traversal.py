from c4game.player import Player
from c4players.mcts.node import Node
import math


class MctsTraversal:

    def __init__(self, root, player, opponent, is_training):
        self.current_node = root
        self.player = player
        self.opponent = opponent
        self.traversed_nodes = [root]
        self.is_training = is_training

    def move(self, board):
        self._update_opponents_move(board)
        self._add_child_nodes_if_necessary(self.current_node, board, self.player.player_id)

        best_move_node = self.current_node.highest_ucb_child() \
            if self.is_training \
            else self.current_node.best_score_child()

        self._set_next_node(best_move_node)

        return self.current_node.col

    def end_game(self, winner):
        win = winner == self.player
        draw = winner is None
        score = 1 if win else 0 if draw else -1
        opponent_score = score * -1

        for node in self.traversed_nodes:
            node.visits += 1
            node.score += score if node.player_id == self.player.player_id else opponent_score

    def _update_opponents_move(self, board):
        if board.last_column_played() is not None:
            matching_nodes = filter(lambda node: node.col == board.last_column_played(), self.current_node.children)
            opponent_node = next(matching_nodes, None)
            if opponent_node is None:
                opponent_node = Node(self.current_node, self.opponent.player_id, board.last_column_played)
                self.current_node.children.append(opponent_node)

            self._set_next_node(opponent_node)

    def _set_next_node(self, node):
        self.traversed_nodes.append(node)
        self.current_node = node

    @staticmethod
    def _add_child_nodes_if_necessary(parent, board, player_id):
        if parent.is_leaf():
            parent.children = []
            possible_moves = board.get_valid_moves()
            for move in possible_moves:
                child = Node(parent, player_id, move)
                parent.children.append(child)
