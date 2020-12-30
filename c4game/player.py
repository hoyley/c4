from abc import ABC, abstractmethod


class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    @abstractmethod
    def move(self, board):
        pass
