class Game:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.winner = None
        self.game_over = False

    def start_game(self):

        while not self.game_over:
            col = self.current_player.move(self.board)
            self.board.play(col, self.current_player.player_id)

            if self.board.check_win_from_last_move():
                self.winner = self.current_player
                self.game_over = True
            elif not self.board.get_valid_moves():
                self.game_over = True
            else:
                self._alternate_player()

    def _alternate_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
