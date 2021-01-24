from abc import abstractmethod
from typing import Optional, List

from game.action import Action
from game.board import Board
from game.player import Player


class TwoPlayerTurnBasedGame:
    def __init__(self, board: Board, player1: Player, player2: Player, is_training: bool):
        self.board = board
        self.player1: Player = player1
        self.player2: Player = player2
        self.winner: Optional[Player] = None
        self.game_over: bool = False
        self.is_training: bool = is_training

    def start_game(self):
        while not self.game_over:
            player = self.get_current_player()
            action = player.move(self)
            self.board.play(action)

            if self.is_game_over():
                self.game_over = True
                self.winner = self._get_winner()
                self.player1.game_over(self)
                self.player2.game_over(self)

    def get_opponent(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def is_game_over(self):
        return self.game_over or self.board.is_game_over()

    @abstractmethod
    def get_valid_actions(self) -> List[Action]:
        pass

    @abstractmethod
    def get_current_player(self) -> Player:
        pass

    @abstractmethod
    def _get_winner(self) -> Optional[Player]:
        pass