from c4game.player import Player
from c4players.mcts.node import Node
from c4players.mcts.mcts_traversal import MctsTraversal

class MctsPlayer(Player):

    def __init__(self, player_id, _config):
        super().__init__(player_id)
        self.root = Node.create_root()
        self.current_traversal = None

    def move(self, game):
        self._initialize(game)
        return self.current_traversal.move(game.board)

    def game_over(self, game):
        self.current_traversal.end_game(game)
        self.current_traversal = None

    def _initialize(self, game):
        if self.current_traversal is None:
            opponent = game.get_opponent(self)
            self.current_traversal = MctsTraversal(self.root, self, opponent, game.is_training)
