from c4game.player import Player
from c4players.mcts.node import Node
from c4players.mcts.mcts_traversal import MctsTraversal
from pickle import dump, load
import util
import os


class MctsPlayer(Player):
    SAVE_PATH = "checkpoints/mcts.ckpt"

    def __init__(self, player_id, config):
        super().__init__(player_id, config)
        self.root = Node.create_root()
        self.current_traversal = None

        util.create_path(MctsPlayer.SAVE_PATH)
        if self.load_model:
            self.load_state()

    def move(self, game):
        self._initialize(game)
        return self.current_traversal.move(game.board)

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
                load(f)
            print("MCTS model loaded from disk.")

    def _initialize(self, game):
        if self.current_traversal is None:
            opponent = game.get_opponent(self)
            self.current_traversal = MctsTraversal(self.root, self, opponent, game.is_training)


