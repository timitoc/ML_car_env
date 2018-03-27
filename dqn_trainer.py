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
parser.add_argument('--mode', choices=['train', 'test', 'resume'], default='train')
parser.add_argument('--weights', type=str, default=None)
args = parser.parse_args()

env = EnvironmentWrapper(enable_rendering=True)
np.random.seed(14238)
env.seed(14238)
nb_actions = env.action_space.n

model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(312))
model.add(Activation('relu'))
model.add(Dense(156))
model.add(Activation('relu'))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('softmax'))
print(model.summary())

memory = SequentialMemory(limit=100000, window_length=1)
# policy = BoltzmannQPolicy()
if args.mode == 'train':
    policy = LinearAnnealedPolicy(EpsStochasticPolicy(), attr='eps', value_max=1., value_min=.25, value_test=.05,
                                  nb_steps=20000)
else:
    policy = EpsStochasticPolicy(eps=.25)
test_policy = MaxBoltzmannQPolicy(eps=0.1)

# dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=200,
#               enable_dueling_network=True, dueling_type='avg', target_model_update=1e-2, policy=policy)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
               enable_dueling_network=True, dueling_type='avg', target_model_update=1e-2,
               policy=policy, test_policy=test_policy)
dqn.compile(Adam(lr=0.0003, ), metrics=['mae'])

if args.mode == 'resume':
    weights_filename = None
    if args.weights:
        weights_filename = args.weights
    else:
        print "You need to specify a model checkpoint for resuming"
    dqn.load_weights(weights_filename)

if args.mode == 'train' or args.mode == 'resume':
    callbacks = [TestLogger()]
    checkpoint_weights_filename = 'model_checkpoints/dqn_' + env.env_name + '_weights_{step}.h5f'
    callbacks += [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=20000)]
    dqn.fit(env, callbacks=callbacks, nb_steps=3500000, visualize=True, verbose=2)

    # Save weights at the end of training
    dqn.save_weights('model_checkpoints/dqn_' + env.env_name + '_weights_{}.h5f'.format(3500000), overwrite=True)

    # Finally, evaluate our algorithm for 5 episodes.
    dqn.test(env, nb_episodes=5, visualize=True)

else:
    weights_filename = None
    if args.weights:
        weights_filename = args.weights
    else:
        print "You need to specify a model checkpoint for testing"
    dqn.load_weights(weights_filename)
    dqn.test(env, nb_episodes=20, visualize=True)
