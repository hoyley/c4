class Game:
    def __init__(self, board, player1, player2, is_training):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.winner = None
        self.game_over = False
        self.is_training = is_training

    def start_game(self):
        while not self.game_over:
            col = self.current_player.move(self)
            self.board.play(col, self.current_player.player_id)

            if self.board.check_win_from_last_move():
                self.winner = self.current_player
                self._game_over()
            elif not self.board.get_valid_moves():
                self._game_over()
            else:
                self._alternate_player()

    def get_opponent(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def _game_over(self):
        self.game_over = True
        self.player1.game_over(self)
        self.player2.game_over(self)

    def _alternate_player(self):
        self.current_player = self.get_opponent(self.current_player)
