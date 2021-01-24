from typing import List, Tuple

from game.action import Action
from game.board import Board
from game.players.mcts.mcts_strategy import MctsStrategy
from game.two_player_turn_based_game import TwoPlayerTurnBasedGame


class C4MctsStrategy(MctsStrategy):

    def get_opponent_moves_to_advance(self, board: Board) -> List[Action]:
        last_action = board.get_last_action()
        return [last_action] if last_action else []

    def get_scores(self, game: TwoPlayerTurnBasedGame) -> Tuple[int, int]:
        winner = game.winner
        if winner == game.player1:
            return 1, -1
        elif winner == game.player2:
            return -1, 1
        else:
            return 0, 0
