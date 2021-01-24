import unittest

from c4_game.c4_action import C4Action
from c4_game.c4_board import C4Board
from c4_game.c4_game import C4Game
from game.player import Player


class TestC4(unittest.TestCase):

    def test_player1_win(self):
        board = C4Board(4, 4, 3)
        player1 = TestPlayer([0, 0, 0], -1)
        player2 = TestPlayer([1, 1], 1)
        game = C4Game(board, player1, player2, False)

        game.start_game()
        self.assertEqual(player1, game.winner)

    def test_draw(self):
        board = C4Board(4, 4, 3)
        player1 = TestPlayer([0, 3, 1, 2, 0, 3, 1, 2], -1)
        player2 = TestPlayer([1, 2, 0, 3, 1, 2, 0, 3], 1)
        game = C4Game(board, player1, player2, False)

        game.start_game()
        self.assertEqual(None, game.winner)

    def test_undo_move(self):
        board = C4Board(4, 4, 4)
        player1 = TestPlayer([0, 0, 0, 0], -1)
        player2 = TestPlayer([1, 1, 1], 1)
        game = C4Game(board, player1, player2, False)
        game.start_game()

        self.assertEqual(4, board.col_counts[0])
        self.assertEqual(3, board.col_counts[1])
        self.assertEqual(0, board.get_last_action().col)
        board.undo_move()
        self.assertEqual(3, board.col_counts[0])
        self.assertEqual(3, board.col_counts[1])
        self.assertEqual(1, board.get_last_action().col)
        board.undo_move()
        self.assertEqual(3, board.col_counts[0])
        self.assertEqual(2, board.col_counts[1])
        self.assertEqual(0, board.get_last_action().col)
        board.undo_move()
        self.assertEqual(2, board.col_counts[0])
        self.assertEqual(2, board.col_counts[1])
        self.assertEqual(1, board.get_last_action().col)
        board.undo_move()
        self.assertEqual(2, board.col_counts[0])
        self.assertEqual(1, board.col_counts[1])
        self.assertEqual(0, board.get_last_action().col)


class TestPlayer(Player):
    def __init__(self, moves, player_id):
        super().__init__(player_id)
        self.moves = moves

    def move(self, game):
        return C4Action(self.player_id, self.moves.pop())

    def game_over(self, game):
        pass


if __name__ == '__main__':
    unittest.main()
