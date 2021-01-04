from collections import deque

import math
import numpy as np
import os
import random
from keras.layers import Dense
from keras.models import Sequential

from c4game.player import Player


class DqnPlayer(Player):

    def __init__(self, player_id):
        super().__init__(player_id)

        # Hack: https://github.com/dmlc/xgboost/issues/1715
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # decay or discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.tau = .125
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.previous_action = None
        self.previous_state = None

    def move(self, game):
        state, available_moves = self._observe(game)
        self.previous_action = self._act(state, available_moves)
        self.previous_state = state

        return self.previous_action

    def game_over(self, game):
        self._observe(game)

    def _observe(self, game):
        current_state = [item for sublist in game.board.board for item in sublist]
        available_moves = game.board.get_valid_moves()

        if self.previous_state:
            reward = 1 if game.winner is not None and game.winner == self.player_id \
                else -1 if game.winner is not None \
                else 0

            sample = [self.previous_state, self.previous_action, reward, current_state, game.game_over]
            self.memory.append(sample)

            self._replay()
            self._target_train()

        return current_state, available_moves

    def _act(self, state, available_moves):

        if np.random.random() < self._decay_epsilon():
            return random.choice(available_moves)

        prediction = self.model.predict(state)[0]
        # Todo: Issue here. Right now I'm excluding predictions that aren't in the list of available moves,
        #   but I might have to solve this instead by allowing the move and it resulting in a negative reward.
        #   I'm not sure the affect this has on predictions in the replay method as they don't exclude invalid moves
        for i in range(7):
            prediction[i] = prediction[i] if i in available_moves else -math.inf

        return np.argmax(prediction)

    def _replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def _target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def _decay_epsilon(self):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        return self.epsilon

    @staticmethod
    def _build_model():
        # Model not thought through. Just putting in something that works at this point.
        model = Sequential()
        model.add(Dense(24, input_dim=1, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(7))
        model.compile(loss='logcosh', optimizer='rmsprop', metrics=['accuracy'])

        return model
