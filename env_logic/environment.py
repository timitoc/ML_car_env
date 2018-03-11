import pygame

from car import Car
from obstacle import Obstacle
from parking_spot import ParkingSpot
from scene import Scene
from utils.constants import *


class Environment(object):
    def __init__(self, size=[1080, 960], enable_rendering=True):
        self.size = size
        self.enable_rendering = enable_rendering
        if enable_rendering:
            pygame.init()
            self.screen = pygame.display.set_mode(size)
            pygame.display.set_caption("Car parking simulator")
            self.scene = Scene(self.screen)
        else:
            self.scene = Scene(None)
        self.reset()
        pygame.mouse.set_visible(0)

    def step(self, action_value):
        self.scene.update(Action(action_value))
        observation = self.scene.get_observation()
        reward = self.scene.get_reward()
        done = self.scene.check_done()
        info = self.scene.get_auxiliar_info()
        return observation, reward, done, info

    def reset(self):
        self.scene.clear()
        self.scene.add_park(ParkingSpot(3))
        self.scene.set_car(Car())
        self.scene.add_obstacle(Obstacle(1))
        self.scene.add_obstacle(Obstacle(2))
        self.scene.add_obstacle(Obstacle(4))
        return self.scene.get_observation()

    def render(self):
        if not self.enable_rendering:
            return
        self.screen.fill(WHITE)
        self.scene.draw()
        pygame.display.flip()
