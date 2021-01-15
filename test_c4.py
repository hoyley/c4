import unittest
from c4game.board import Board
from c4game.player import Player
from c4game.game import Game


class TestC4(unittest.TestCase):

    def test_player1_win(self):
        board = Board(4, 4, 3)
        player1 = TestPlayer([0, 0, 0], -1)
        player2 = TestPlayer([1, 1], 1)
        game = Game(board, player1, player2, False)

        game.start_game()
        self.assertEqual(player1, game.winner)

    def test_draw(self):
        board = Board(4, 4, 3)
        player1 = TestPlayer([0, 3, 1, 2, 0, 3, 1, 2], -1)
        player2 = TestPlayer([1, 2, 0, 3, 1, 2, 0, 3], 1)
        game = Game(board, player1, player2, False)

        game.start_game()
        self.assertEqual(None, game.winner)

    def test_undo_move(self):
        board = Board(4, 4, 4)
        player1 = TestPlayer([0, 0, 0, 0], -1)
        player2 = TestPlayer([1, 1, 1], 1)
        game = Game(board, player1, player2, False)
        game.start_game()

        self.assertEqual(4, board.col_counts[0])
        self.assertEqual(3, board.col_counts[1])
        self.assertEqual(0, board.last_column_played())
        board.undo_move()
        self.assertEqual(3, board.col_counts[0])
        self.assertEqual(3, board.col_counts[1])
        self.assertEqual(1, board.last_column_played())
        board.undo_move()
        self.assertEqual(3, board.col_counts[0])
        self.assertEqual(2, board.col_counts[1])
        self.assertEqual(0, board.last_column_played())
        board.undo_move()
        self.assertEqual(2, board.col_counts[0])
        self.assertEqual(2, board.col_counts[1])
        self.assertEqual(1, board.last_column_played())
        board.undo_move()
        self.assertEqual(2, board.col_counts[0])
        self.assertEqual(1, board.col_counts[1])
        self.assertEqual(0, board.last_column_played())


class TestPlayer(Player):
    def __init__(self, moves, player_id):
        super().__init__(player_id)
        self.moves = moves

    def move(self, game):
        return self.moves.pop()

    def game_over(self, game):
        pass


if __name__ == '__main__':
    unittest.main()
