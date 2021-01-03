import math
import util
import random


class Node:
    def __init__(self, parent, player_id, col):
        self.parent = parent
        self.player_id = player_id
        self.col = col
        self.visits = 0
        self.score = 0
        self.children = []

    def is_leaf(self):
        return self.children == []

    def ucb(self):
        if self.visits == 0 or self.parent is None:
            return math.inf
        return self.score/self.visits + (math.log(self.parent.visits) / self.visits)

    def probability(self):
        return self.score / self.visits if self.visits != 0 else 0

    def highest_ucb_child(self):
        if not self.is_leaf():
            max_children = util.max_list(self.children, key_func=lambda child: child.ucb())
            return random.choice(max_children)

    def best_score_child(self):
        if not self.is_leaf():
            max_children = util.max_list(self.children, key_func=lambda child: child.probability())
            return random.choice(max_children)

    @staticmethod
    def create_root():
        return Node(None, None, None)
