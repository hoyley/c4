from game.player import Player


class C4HumanPlayer(Player):

    def move(self, game):
        print()
        print(" --------------------------------- ")
        print("  It's your turn! ")
        print(" --------------------------------- ")
        print()
        game.board.print_replace('X', 'O', '.')
        print()
        print("Enter your choice: {}".format(game.board.get_valid_moves()))

        return C4HumanPlayer.get_input(game.board)

    def _on_game_over(self, game):
        print()
        print(" --------------------------------- ")
        if game.winner is None:
            print(" Tie Game!")
        elif game.winner == self:
            print(" You won!!!")
        else:
            print(" You lost :(")
        print(" --------------------------------- ")
        print()
        game.board.print_replace('X', 'O', '.')
        print()
        print("*** GAME OVER ***")

    @staticmethod
    def get_input(board):
        while True:
            try:
                choice = int(input())
                if choice not in board.get_valid_moves():
                    print("Invalid selection")
                    continue
                break
            except ValueError:
                print("Invalid selection")
                continue

        return choice




