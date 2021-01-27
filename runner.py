import math
import sys

from c4_game.c4_game_factory import C4GameFactory
from c4_game.c4_players.player_factory import PlayerFactory
from game.series import Series


def read_command(argv):
    from optparse import OptionParser
    usage = """
        USAGE:      python runner.py <options>
    """
    parser = OptionParser(usage)

    parser.add_option('-t', '--numTraining', dest='num_training', type='int', default=100000)
    parser.add_option('-n', '--numGames', dest='num_games', type='int', default=50)
    parser.add_option('-r', '--numRows', dest='num_rows', type='int', default=6)
    parser.add_option('-c', '--numCols', dest='num_cols', type='int', default=7)
    parser.add_option('-x', '--lineLength', dest='line_length', type='int', default=4)
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
    args['num_rows'] = options.num_rows
    args['num_cols'] = options.num_cols
    args['line_length'] = options.line_length
    args['print_buffer'] = options.print_buffer

    try:
        args['player1'] = PlayerFactory.create(options.p1_strategy, player_id=-1,
                                               config={'load_model': options.load_models,
                                                       'store_freq': options.store_model_freq})
    except ValueError as ex:
        print(ex)
        raise ValueError('Player 1 strategy is invalid: {}'.format(options.p1_strategy)) from ex

    try:
        args['player2'] = PlayerFactory.create(options.p2_strategy, player_id=1,
                                               config={'load_model': options.load_models,
                                                       'store_freq': options.store_model_freq})
    except ValueError as ex:
        print(ex)
        raise ValueError('Player 2 strategy is invalid: {}'.format(options.p2_strategy)) from ex

    return args


def run_command(player1, player2, num_training, num_games, num_rows, num_cols, line_length, print_buffer):
    game_factory = C4GameFactory(player1, player2, num_rows, num_cols, line_length)

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
        print(ex)
        sys.exit(0)

    try:
        run_command(**parsed_args)
    except KeyboardInterrupt:
        print()
        print("Quitter!")

