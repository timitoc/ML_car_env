from collections import deque

import argparse
import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, Adadelta

from rl.agents.dqn import DQNAgent
from rl.callbacks import Callback, ModelIntervalCheckpoint
from rl.policy import BoltzmannQPolicy, LinearAnnealedPolicy, EpsGreedyQPolicy, MaxBoltzmannQPolicy
from rl.memory import SequentialMemory

from bridge import EnvironmentWrapper
from epsStochastic import EpsStochasticPolicy


class TestLogger(Callback):

    def __init__(self):
        super(TestLogger, self).__init__()
        self.scores = deque(maxlen=100)

    def on_train_begin(self, logs):
        print "Train begin callback xD"

    def on_episode_end(self, episode, logs):
        self.scores.append(int(logs['episode_reward']))
        template = 'Episode {0}: reward: {1:.3f}, last_100_mean: {2}'
        variables = [
            episode + 1,
            logs['episode_reward'],
            np.mean(self.scores),
        ]
        print(template.format(*variables))

parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['train', 'test'], default='train')
parser.add_argument('--weights', type=str, default=None)
args = parser.parse_args()

env = EnvironmentWrapper(enable_rendering=True)
# Get the environment and extract the number of actions.
# np.random.seed(14238)
# env.seed(14238)
nb_actions = env.action_space.n

# Next, we build a very simple model regardless of the dueling architecture
# if you enable dueling network in DQN , DQN will build a dueling network base on your model automatically
# Also, you can build a dueling network by yourself and turn off the dueling network in DQN.
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('softmax'))
print(model.summary())


memory = SequentialMemory(limit=100000, window_length=1)
# policy = BoltzmannQPolicy()
policy = LinearAnnealedPolicy(MaxBoltzmannQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                              nb_steps=20000)
test_policy = MaxBoltzmannQPolicy(eps=0.1)
# enable the dueling network
# you can specify the dueling_type to one of {'avg','max','naive'}
# dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=200,
#               enable_dueling_network=True, dueling_type='avg', target_model_update=1e-2, policy=policy)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
               enable_dueling_network=True, dueling_type='avg', target_model_update=1e-2,
               policy=policy, test_policy=test_policy)
dqn.compile(Adam(lr=0.0005, ), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.

if args.mode == 'train':
    callbacks = [TestLogger()]
    checkpoint_weights_filename = 'model_checkpoints/dqn_' + env.env_name + '_weights_{step}.h5f'
    callbacks += [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=20000)]
    dqn.fit(env, callbacks=callbacks, nb_steps=2500000, visualize=True, verbose=2)

    # Save weights at the end of training
    dqn.save_weights('model_checkpoints/dqn_' + env.env_name + '_weights_{}.h5f'.format(2500000), overwrite=True)

    # Finally, evaluate our algorithm for 5 episodes.
    dqn.test(env, nb_episodes=5, visualize=True)

else:
    weights_filename = None
    if args.weights:
        weights_filename = args.weights
    else:
        print "You need to specify a model checkpoint for testing"
    dqn.load_weights(weights_filename)
    dqn.test(env, nb_episodes=10, visualize=True)



