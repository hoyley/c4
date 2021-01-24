from game.players.mcts.mcts_strategy import MctsStrategy


class LcMctsStrategy(MctsStrategy):

    def get_opponent_moves_to_advance(self, board):
        return board.get_last_opponent_actions()

    def get_scores(self, game):
        return game.board.player_1_state.score(), game.board.player_2_state.score()
