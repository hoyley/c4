import math
import sys
import traceback

from game.series import Series
from lc_game.constants import PLAYER_2, PLAYER_1
from lc_game.game_factory import LcGameFactory
from lc_game.lc_players import LcMctsStrategy
from game.players.random_player import RandomPlayer
from game.players.mcts.mcts_player import MctsPlayer


class LcMctsPlayer(object):
    pass


def read_command(argv):
    from optparse import OptionParser
    usage = """
        USAGE:      python lc_runner.py <options>
    """
    parser = OptionParser(usage)

    parser.add_option('-t', '--numTraining', dest='num_training', type='int', default=100000)
    parser.add_option('-n', '--numGames', dest='num_games', type='int', default=50)
    parser.add_option('-p', '--printBuffer', dest='print_buffer', type='int', default=1000)
    parser.add_option('-a', '--p1strategy', dest='p1_strategy', type='string', default='<NOT_SPECIFIED>')
    parser.add_option('-b', '--p2strategy', dest='p2_strategy', type='string', default='<NOT_SPECIFIED>')
    parser.add_option('-s', '--store_model_freq', dest='store_model_freq', type='int', default=math.inf)
    parser.add_option("-l", action="store_true", dest="load_models")

    options, other_junk = parser.parse_args(argv)

    if len(other_junk) != 0:
        raise Exception('Command line input not understood: ' + str(other_junk))

    args = dict()
    args['num_training'] = options.num_training
    args['num_games'] = options.num_games
    args['print_buffer'] = options.print_buffer

    args['player2'] = MctsPlayer(PLAYER_2, LcMctsStrategy())
    args['player1'] = RandomPlayer(PLAYER_1) # SplitPlayer(PLAYER_2, RandomPlayer(PLAYER_2), HumanPlayer(PLAYER_2))

    return args


def run_command(player1, player2, num_training, num_games, print_buffer):
    game_factory = LcGameFactory(player1, player2)

    print()
    print('Training...')
    series = Series(num_training, player1, player2, game_factory=game_factory, is_training=True,
                    print_buffer=print_buffer)
    series.play()
    series.print_results()

    print()
    print('Playing...')
    series = Series(num_games, player1, player2, game_factory=game_factory, is_training=False,
                    print_buffer=print_buffer)
    series.play()
    series.print_results()


if __name__ == '__main__':
    try:
        parsed_args = read_command(sys.argv[1:])  # Get game components based on input
    except Exception as ex:
        traceback.print_exc()
        sys.exit(0)

    try:
        run_command(**parsed_args)
    except KeyboardInterrupt:
        print()
        print("Quitter!")

