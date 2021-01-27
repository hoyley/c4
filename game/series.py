import datetime
import math
import sys
import time

from game.game_factory import GameFactory
from game.player import Player


class Series:

    def __init__(self, num_games: int, player1: Player, player2: Player, game_factory: GameFactory,
                 is_training: bool = False, print_buffer: int = sys.maxsize):
        self._num_games = num_games
        self._player1 = player1
        self._player2 = player2
        self._game_factory = game_factory
        self._start_time = time.time()
        self._is_training = is_training
        self._print_buffer = print_buffer
        self._last_batch_p1_wins = 0
        self._last_batch_p2_wins = 0
        self._last_batch_ties = 0
        self._last_batch_games_played = 0
        self._last_batch_start_time = time.time()
        self.results_ties = 0
        self.results_player1_wins = 0
        self.results_player2_wins = 0
        self.games_played = 0
        self.total_time = None

    def play(self):
        for game_num in range(self._num_games):
            game = self._start_game()
            self._game_over(game)

        self.total_time = time.time() - self._start_time

    def print_results(self):
        if self.games_played:
            print()
            print('--- Summary ---')
            print(self._format_summary())

    def _start_game(self):
        game = self._game_factory.create_game(self._is_training)
        game.start_game()
        return game

    def _game_over(self, game):
        if game.winner == self._player1:
            self.results_player1_wins += 1
        elif game.winner == self._player2:
            self.results_player2_wins += 1
        else:
            self.results_ties += 1
        self.games_played += 1

        if self.games_played % self._print_buffer == 0:
            print(self._format_batch())

    def _format_batch(self):
        output = Series._format_result(self._start_time,
                                       self.results_player1_wins - self._last_batch_p1_wins,
                                       self.results_player2_wins - self._last_batch_p2_wins,
                                       self.results_ties - self._last_batch_ties,
                                       self.games_played,
                                       self._num_games,
                                       self.games_played - self._last_batch_games_played,
                                       self._last_batch_start_time)

        self._last_batch_p1_wins = self.results_player1_wins
        self._last_batch_p2_wins = self.results_player2_wins
        self._last_batch_ties = self.results_ties
        self._last_batch_games_played = self.games_played
        self._last_batch_start_time = time.time()

        return output

    def _format_summary(self):
        return Series._format_result(self._start_time,
                                     self.results_player1_wins,
                                     self.results_player2_wins,
                                     self.results_ties,
                                     self.games_played,
                                     self._num_games,
                                     self._num_games,
                                     self._start_time)

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

