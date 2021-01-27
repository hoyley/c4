import os
from pickle import dump, load

from game.player import Player
from game.players.mcts.mcts_traversal import MctsTraversal
from game.players.mcts.node import Node
from game.util import create_path


class MctsPlayer(Player):
    SAVE_PATH = "checkpoints/mcts.ckpt"

    def __init__(self, player_id, mcts_strategy, config=None):
        super().__init__(player_id, config)
        self.root = Node.create_root()
        self.current_traversal = None
        self.mcts_strategy = mcts_strategy

        create_path(MctsPlayer.SAVE_PATH)
        if self._load_model:
            self.load_state()

    def move(self, game):
        self._initialize(game)
        return self.current_traversal.move(game)

    def _on_game_over(self, game):
        self.current_traversal.end_game(game)
        self.current_traversal = None

    def save_state(self):
        with open(MctsPlayer.SAVE_PATH, "wb") as f:
            dump(self.root, f)
        print("MCTS model saved to disk.")

    def load_state(self):
        if os.path.exists(MctsPlayer.SAVE_PATH):
            with open(MctsPlayer.SAVE_PATH, "rb") as f:
                self.root = load(f)
            print("MCTS model loaded from disk.")

    def _initialize(self, game):
        if self.current_traversal is None:
            opponent = game.get_opponent(self)
            self.current_traversal = MctsTraversal(self.mcts_strategy, self.root, self, opponent, game.is_training)


