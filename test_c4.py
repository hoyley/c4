import unittest

from c4_game.c4_action import C4Action
from c4_game.c4_board import C4Board
from c4_game.c4_game import C4Game
from c4_game.c4_game_factory import C4GameFactory
from c4_game.c4_players.player_factory import PlayerFactory
from game.player import Player
from game.series import Series


class TestC4(unittest.TestCase):

    def test_player1_win(self):
        board = C4Board(4, 4, 3)
        player1 = TestPlayer([0, 0, 0], C4Board.PLAYER_1_TOKEN)
        player2 = TestPlayer([1, 1], C4Board.PLAYER_2_TOKEN)
        game = C4Game(board, player1, player2, False)

        game.start_game()
        self.assertEqual(player1, game.winner)

    def test_draw(self):
        board = C4Board(4, 4, 3)
        player1 = TestPlayer([0, 3, 1, 2, 0, 3, 1, 2], C4Board.PLAYER_1_TOKEN)
        player2 = TestPlayer([1, 2, 0, 3, 1, 2, 0, 3], C4Board.PLAYER_2_TOKEN)
        game = C4Game(board, player1, player2, False)

        game.start_game()
        self.assertEqual(None, game.winner)

    def test_undo_move(self):
        board = C4Board(4, 4, 4)
        player1 = TestPlayer([0, 0, 0, 0], C4Board.PLAYER_1_TOKEN)
        player2 = TestPlayer([1, 1, 1], C4Board.PLAYER_2_TOKEN)
        game = C4Game(board, player1, player2, False)
        game.start_game()

        self.assertEqual(4, board.col_counts[0])
        self.assertEqual(3, board.col_counts[1])
        self.assertEqual(0, board.get_last_action().col)
        board.undo_action()
        self.assertEqual(3, board.col_counts[0])
        self.assertEqual(3, board.col_counts[1])
        self.assertEqual(1, board.get_last_action().col)
        board.undo_action()
        self.assertEqual(3, board.col_counts[0])
        self.assertEqual(2, board.col_counts[1])
        self.assertEqual(0, board.get_last_action().col)
        board.undo_action()
        self.assertEqual(2, board.col_counts[0])
        self.assertEqual(2, board.col_counts[1])
        self.assertEqual(1, board.get_last_action().col)
        board.undo_action()
        self.assertEqual(2, board.col_counts[0])
        self.assertEqual(1, board.col_counts[1])
        self.assertEqual(0, board.get_last_action().col)

    def test_random_v_random(self):
        num_games = 500
        expected_win_proximity_percentage = 20
        player1 = PlayerFactory().create("random", C4Board.PLAYER_1_TOKEN)
        player2 = PlayerFactory().create("random", C4Board.PLAYER_2_TOKEN)
        game_factory = C4GameFactory(player1, player2)

        series = Series(num_games, player1, player2, game_factory=game_factory, is_training=True)
        series.play()
        self.assertEqual(num_games, series.games_played)

        win_proximity_percentage = abs(series.results_player1_wins - series.results_player2_wins) / num_games * 100
        self.assertLessEqual(win_proximity_percentage, expected_win_proximity_percentage,
                             "Expected player 1 and player 2 to win within {} percent of games but difference was {} "
                             "percent of games. This could be an improbable occurrence, try running tests again."
                             .format(expected_win_proximity_percentage, win_proximity_percentage))

    def test_minimax_v_random(self):
        num_games = 20
        expected_win_percentage = 90
        player1 = PlayerFactory().create("minimax", C4Board.PLAYER_1_TOKEN)
        player2 = PlayerFactory().create("random", C4Board.PLAYER_2_TOKEN)
        game_factory = C4GameFactory(player1, player2)

        series = Series(num_games, player1, player2, game_factory=game_factory, is_training=True)
        series.play()
        self.assertEqual(num_games, series.games_played)

        win_percentage = series.results_player1_wins / num_games * 100
        self.assertGreaterEqual(win_percentage, expected_win_percentage,
                                "Expected minimax to beat random in {} percent of games but actual was {} "
                                "percent of games. This could be an improbable occurrence, try running tests again."
                                .format(expected_win_percentage, win_percentage))

    def test_mcts_v_random(self):
        num_training = 10000
        num_games = 100
        expected_win_percentage = 70
        player1 = PlayerFactory().create("mcts", C4Board.PLAYER_1_TOKEN)
        player2 = PlayerFactory().create("random", C4Board.PLAYER_2_TOKEN)
        game_factory = C4GameFactory(player1, player2)

        training = Series(num_training, player1, player2, game_factory=game_factory, is_training=True)
        training.play()
        series = Series(num_games, player1, player2, game_factory=game_factory, is_training=False)
        series.play()
        self.assertEqual(num_games, series.games_played)

        win_percentage = series.results_player1_wins / num_games * 100
        self.assertGreaterEqual(win_percentage, expected_win_percentage,
                                "Expected mcts to beat random in {} percent of games but actual was {} "
                                "percent of games. This could be an improbable occurrence, try running tests again."
                                .format(expected_win_percentage, win_percentage))

    def test_dqn_v_random(self):
        num_games = 10
        expected_win_percentage = 40
        player1 = PlayerFactory().create("dqn", C4Board.PLAYER_1_TOKEN)
        player2 = PlayerFactory().create("random", C4Board.PLAYER_2_TOKEN)
        game_factory = C4GameFactory(player1, player2)

        series = Series(num_games, player1, player2, game_factory=game_factory, is_training=True)
        series.play()
        self.assertEqual(num_games, series.games_played)

        win_percentage = series.results_player1_wins / num_games * 100
        self.assertGreaterEqual(win_percentage, expected_win_percentage,
                                "Expected minimax to beat random in {} percent of games but actual was {} "
                                "percent of games. This could be an improbable occurrence, try running tests again."
                                .format(expected_win_percentage, win_percentage))


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
