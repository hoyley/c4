from c4game.game import Game
from c4game.board import Board
from c4game.board_factory import BoardFactory
import time


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

    def play(self):
        for game_num in range(self.num_games):
            board = self.board_factory.create()
            game = Game(board, self.player1, self.player2, self.is_training)
            game.start_game()
            winner = game.winner.player_id if game.winner else 0
            self.results[winner] += 1
            self.games_played += 1

            if game_num % self.print_buffer == self.print_buffer - 1:
                self.print_result()

        self.total_time = time.time() - self.start_time

    def print_result(self):
        total_time = time.time() - self.start_time
        p1_wins = self.results[self.player1.player_id]
        p2_wins = self.results[self.player2.player_id]
        ties = self.results[Board.EMPTY_TOKEN]

        print('Time: {:0.4f} -- Games Played: {}/{} -- P1 Wins: {} -- P2 Wins: {} -- Ties: {} -- Avg Time: {:04f} '
              '-- P1% {:0.2f} -- P2% {:0.2f} -- Tie% {:0.2f}'
              .format(total_time, self.games_played, self.num_games, p1_wins, p2_wins, ties,
                      total_time / self.games_played,
                      p1_wins / self.games_played * 100,
                      p2_wins / self.games_played * 100,
                      ties / self.games_played * 100))

    def print_results(self):
        print()
        print('--- Summary ---')

        self.print_result()

        if self.num_games > 0:
            print('P1 Win %: {:0.3f}% -- P2 Win %: {:0.3f}% -- Tie %: {:0.3f}% -- Time per game: {:0.5f}'.format(
                self.results[self.player1.player_id] / self.num_games * 100,
                self.results[self.player2.player_id] / self.num_games * 100,
                self.results[0] / self.num_games * 100,
                self.total_time / self.num_games
            ))
