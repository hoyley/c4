import unittest
from c4game.board import Board
from c4game.player import Player
from c4game.game import Game


class TestC4(unittest.TestCase):

    def test_player1_win(self):
        board = Board(4, 4, 3)
        player1 = TestPlayer([0, 0, 0, 0], -1)
        player2 = TestPlayer([1, 1, 1], 1)
        game = Game(board, player1, player2)

        game.start_game()
        self.assertEqual(player1, game.winner)

    def test_draw(self):
        board = Board(4, 4, 3)
        player1 = TestPlayer([0, 3, 1, 2, 0, 3, 1, 2], -1)
        player2 = TestPlayer([1, 2, 0, 3, 1, 2, 0, 3], 1)
        game = Game(board, player1, player2)

        game.start_game()
        self.assertEqual(None, game.winner)


class TestPlayer(Player):
    def __init__(self, moves, player_id):
        super().__init__(player_id)
        self.moves = moves

    def move(self, board):
        return self.moves.pop()


if __name__ == '__main__':
    unittest.main()
