from game.board import Board
from game.two_player_turn_based_game import TwoPlayerTurnBasedGame


class MctsTraversal:

    def __init__(self, mcts_strategy, root, player, opponent, is_training):
        self.current_node = root
        self.player = player
        self.opponent = opponent
        self.is_training = is_training
        self.mcts_strategy = mcts_strategy

    def move(self, game: TwoPlayerTurnBasedGame):
        self._update_opponents_move(game.board)

        valid_actions = game.get_valid_actions()
        self._add_child_nodes_if_necessary(valid_actions)

        best_move_node = self.current_node.highest_ucb_child(valid_actions) \
            if self.is_training \
            else self.current_node.best_score_child(valid_actions)

        self._set_next_node(best_move_node)

        return self.current_node.action

    def end_game(self, game):
        current_player_id = game.get_current_player().player_id
        if current_player_id != self.current_node.player_id:
            self._update_opponents_move(game.board)

        player_1_score, player_2_score = self.mcts_strategy.get_scores(game)
        score_diff = abs(player_1_score - player_2_score)
        winner_id = game.winner.player_id if game.winner else None
        win = winner_id == self.current_node.player_id
        score = score_diff if win else -score_diff

        self.current_node.update_score(score, -score)

    def _update_opponents_move(self, board):
        opponent_actions = self.mcts_strategy.get_opponent_moves_to_advance(board)

        for action in opponent_actions:
            self._advance_move(action)

    def _advance_move(self, action):
        child_node = self.current_node.children.get(action)
        if not child_node:
            child_node = self.current_node.add_child(action.player_id, action)
        self._set_next_node(child_node)

    def _set_next_node(self, node):
        self.current_node = node

    def _add_child_nodes_if_necessary(self, valid_actions):
        for action in valid_actions:
            child_node = self.current_node.children.get(action)
            if not child_node:
                self.current_node.add_child(self.player.player_id, action)
