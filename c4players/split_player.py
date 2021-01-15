from c4game.player import Player


class SplitPlayer(Player):

    def __init__(self, player_id, trainer, player):
        super().__init__(player_id)
        self.player = player
        self.trainer = trainer

    def move(self, game):
        if game.is_training:
            return self.trainer.move(game)
        else:
            return self.player.move(game)

    def game_over(self, game):
        if game.is_training:
            return self.trainer.game_over(game)
        else:
            return self.player.game_over(game)