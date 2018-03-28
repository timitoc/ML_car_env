import numpy as np
from gym import spaces
from rl.core import Env

from env_logic.environment import Environment


class EnvironmentWrapper(Env):
    def __init__(self, enable_rendering=False):
        self.env_name = 'CarPark-v0'
        self.env = Environment(enable_rendering=enable_rendering)
        self.action_space = spaces.Discrete(6)
        low = np.array([
            0,
            -1,
            0, -1,
            0, -1,
            0, -1,
            0, -1,
            0, -1
            # -self.env.size[0], self.env.size[1],
            # -self.env.size[0], -self.env.size[1],
            # -self.env.size[0], -self.env.size[1],
            # -self.env.size[0], -self.env.size[1],
            # -self.env.size[0], -self.env.size[1],
        ])
        high = np.array([
            1,
            1,
            1, 1,
            1, 1,
            1, 1,
            1, 1,
            1, 1
            # self.env.size[0], self.env.size[1],
            # self.env.size[0], self.env.size[1],
            # self.env.size[0], self.env.size[1],
            # self.env.size[0], self.env.size[1],
            # self.env.size[0], self.env.size[1]
        ])
        self.observation_space = spaces.Box(low, high)

    def close(self):
        pass

    def step(self, action):
        return self.env.step(action)

    def render(self, mode='human', close=False):
        self.env.render()

    def reset(self):
        return self.env.reset()

    def configure(self, *args, **kwargs):
        pass

    def seed(self, seed=None):
        pass
