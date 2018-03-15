import gym
import numpy as np
from gym import spaces
from rl.core import Env

from env_logic.environment import Environment


class EnvironmentWrapper(Env):
    def __init__(self, enable_rendering=False):
        self.env_name = 'CarPark-v0'
        self.env = Environment(enable_rendering=enable_rendering)
        self.action_space = spaces.Discrete(9)
        # self.env_name = 'CartPole-v1'
        # self.env = gym.make(self.env_name)
        # self.action_space = self.env.action_space
        low = np.array([
            0,
            -8,
            0, 0
            # -self.env.size[0], self.env.size[1],
            # -self.env.size[0], -self.env.size[1],
            # -self.env.size[0], -self.env.size[1],
            # -self.env.size[0], -self.env.size[1],
            # -self.env.size[0], -self.env.size[1],
        ])
        high = np.array([
            360,
            8,
            self.env.size[0], self.env.size[1]
            # self.env.size[0], self.env.size[1],
            # self.env.size[0], self.env.size[1],
            # self.env.size[0], self.env.size[1],
            # self.env.size[0], self.env.size[1],
            # self.env.size[0], self.env.size[1]
        ])
        self.observation_space = spaces.Box(low, high)
        # self.observation_space = self.env.observation_space

    def close(self):
        pass

    def step(self, action):
        # print action
        return self.env.step(action)

    def render(self, mode='human', close=False):
        self.env.render()

    def reset(self):
        return self.env.reset()

    def configure(self, *args, **kwargs):
        pass

    def seed(self, seed=None):
        pass
