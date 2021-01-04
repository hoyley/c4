from c4game.game import Game
from c4game.board import Board
from c4game.board_factory import BoardFactory
import time


class Series:

    def __init__(self, num_games, player1, player2, is_training=False, board_factory=BoardFactory(), verbose=True):
        self.num_games = num_games
        self.games_played = 0
        self.player1 = player1
        self.player2 = player2
        self.board_factory = board_factory
        self.start_time = time.time()
        self.verbose = verbose
        self.total_time = None
        self.is_training = is_training
        self.results = {0: 0,
                        self.player1.player_id: 0,
                        self.player2.player_id: 0}

    def play(self):
        for game_num in range(self.num_games):
            board = self.board_factory.create()
            game = Game(board, self.player1, self.player2, self.is_training)
            game.start_game()
            winner = game.winner.player_id if game.winner else 0
            self.results[winner] += 1
            self.games_played += 1

            if self.verbose:
                print('Time: {:0.4f} -- Games Played: {}/{} -- Player1 Wins: {} -- Player2 Wins: {} -- Ties: {}'
                      .format(time.time() - self.start_time, game_num + 1, self.num_games,
                              self.results[self.player1.player_id],
                              self.results[self.player2.player_id], self.results[0]))

        self.total_time = time.time() - self.start_time

    def print_results(self):
        print()
        print('--- Summary ---')

        print('Time: {:0.4f} -- Games Played: {}/{} -- Player1 Wins: {} -- Player2 Wins: {} -- Ties: {}'
              .format(time.time() - self.start_time, self.games_played, self.num_games,
                      self.results[self.player1.player_id],
                      self.results[self.player2.player_id], self.results[0]))

        print('P1 Win %: {:0.3f}% -- P2 Win %: {:0.3f}% -- Tie %: {:0.3f}% -- Time per game: {:0.5f}'.format(
            self.results[self.player1.player_id] / self.num_games * 100,
            self.results[self.player2.player_id] / self.num_games * 100,
            self.results[0] / self.num_games * 100,
            self.total_time / self.num_games
        ))
