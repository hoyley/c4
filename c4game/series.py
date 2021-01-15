from c4game.game import Game
from c4game.board import Board
from c4game.board_factory import BoardFactory
import time
import datetime
import math


class Series:

    def __init__(self, num_games, player1, player2, is_training=False, board_factory=BoardFactory(), print_buffer=1000):
        self.num_games = num_games
        self.games_played = 0
        self.player1 = player1
        self.player2 = player2
        self.board_factory = board_factory
        self.start_time = time.time()
        self.total_time = None
        self.is_training = is_training
        self.print_buffer = print_buffer
        self.results = {0: 0,
                        self.player1.player_id: 0,
                        self.player2.player_id: 0}
        self._last_batch_p1_wins = 0
        self._last_batch_p2_wins = 0
        self._last_batch_ties = 0
        self._last_batch_games_played = 0
        self._last_batch_start_time = time.time()

    def play(self):
        for game_num in range(self.num_games):
            game = self._start_game()
            self._game_over(game)

        self.total_time = time.time() - self.start_time

    def print_results(self):
        if self.games_played:
            print()
            print('--- Summary ---')
            print(self._format_summary())

    def _start_game(self):
        board = self.board_factory.create()
        game = Game(board, self.player1, self.player2, self.is_training)
        game.start_game()
        return game

    def _game_over(self, game):
        winner = game.winner.player_id if game.winner else 0
        self.results[winner] += 1
        self.games_played += 1

        if self.games_played % self.print_buffer == 0:
            print(self._format_batch())

    def _format_batch(self):
        output = Series._format_result(self.start_time,
                                       self.results[self.player1.player_id] - self._last_batch_p1_wins,
                                       self.results[self.player2.player_id] - self._last_batch_p2_wins,
                                       self.results[Board.EMPTY_TOKEN] - self._last_batch_ties,
                                       self.games_played,
                                       self.num_games,
                                       self.games_played - self._last_batch_games_played,
                                       self._last_batch_start_time)

        self._last_batch_p1_wins = self.results[self.player1.player_id]
        self._last_batch_p2_wins = self.results[self.player2.player_id]
        self._last_batch_ties = self.results[Board.EMPTY_TOKEN]
        self._last_batch_games_played = self.games_played
        self._last_batch_start_time = time.time()

        return output

    def _format_summary(self):
        return Series._format_result(self.start_time,
                                     self.results[self.player1.player_id],
                                     self.results[self.player2.player_id],
                                     self.results[Board.EMPTY_TOKEN],
                                     self.games_played,
                                     self.num_games,
                                     self.num_games,
                                     self.start_time)

    @staticmethod
    def _format_result(start_time, p1_wins, p2_wins, ties, total_games_played, max_games, batch_games_played,
                       batch_start_time):
        total_time = time.time() - start_time
        batch_time = time.time() - batch_start_time
        percent = total_games_played / max_games * 100
        remaining = math.floor((total_time / total_games_played) * (max_games - total_games_played))

        return '{:0.2f}% -- Time: {:0.4f} -- Est Rem: {} -- Games Played: {}/{} -- P1 Wins: {} ({:0.2f}%) ' \
               '-- P2 Wins: {} ({:0.2f}%) -- Ties: {} ({:0.2f}%) -- Avg Time: {:04f}'\
               .format(percent, total_time, str(datetime.timedelta(0, remaining)),
                       total_games_played, max_games,
                       p1_wins, p1_wins / batch_games_played * 100,
                       p2_wins, p2_wins / batch_games_played * 100,
                       ties, ties / batch_games_played * 100, batch_time / batch_games_played)

