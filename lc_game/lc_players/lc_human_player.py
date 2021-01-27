from game.player import Player
from lc_game.console_utils import ConsoleUtils


class LcHumanPlayer(Player):

    def move(self, game):
        last_action = game.board.get_last_action()
        if last_action and last_action.player_id != self.player_id:
            print("Opponent took actions: {} -- {}".format(game.board.last_action[-2].format(),
                                                           game.board.last_action[-1].format()))

        ConsoleUtils.print_board(game.board)

        actions = game.board.get_valid_actions()
        for i in range(len(actions)):
            print("[{}] {}".format(i, actions[i].format()))
        action_num = LcHumanPlayer.get_input(len(actions))
        return actions[action_num]

    @staticmethod
    def get_input(max_input):
        while True:
            try:
                choice = int(input())
                if choice >= max_input:
                    print("Invalid index")
                    continue
                break
            except ValueError:
                print("Invalid selection")
                continue

        return choice
