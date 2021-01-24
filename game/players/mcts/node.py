import math
import random

from game.util import max_list


class Node:
    EXPLORATION = 1.5

    def __init__(self, parent, player_id, action):
        self.parent = parent
        self.children = {}
        self.player_id = player_id
        self.action = action
        self.visits = 0
        self.score = 0

    def add_child(self, player_id, action):
        child = Node(self, player_id, action)
        self.children[action] = child
        return child

    def is_leaf(self):
        return self.children == {}

    def ucb(self):
        if self.parent is None:
            return math.inf

        my_visits = 1 + self.visits
        parent_visits = 1 + self.parent.visits
        exploration = Node.EXPLORATION if self.score >= 0 else 1/Node.EXPLORATION

        return self.score/my_visits + exploration * ((math.log(parent_visits) / my_visits) ** .5)

    def probability(self):
        return self.score / self.visits if self.visits != 0 else 0

    def highest_ucb_child(self, valid_actions):
        if not self.is_leaf():
            matching_child_nodes = [self.children[action] for action in valid_actions]
            max_children = max_list(matching_child_nodes, key_func=lambda child: child.ucb())
            return random.choice(max_children)

    def best_score_child(self, valid_actions):
        if not self.is_leaf():
            matching_child_nodes = [self.children[action] for action in valid_actions]
            max_children = max_list(matching_child_nodes, key_func=lambda child: child.probability())
            return random.choice(max_children)

    def update_score(self, score, opponent_score):
        # This method would be cleaner as a recursive method, but should perform better this way
        current_node = self

        while current_node:
            current_node.visits += 1
            if current_node.player_id == self.player_id:
                current_node.score += score
            else:
                current_node.score += opponent_score
            current_node = current_node.parent

    @staticmethod
    def create_root():
        return Node(None, None, None)
