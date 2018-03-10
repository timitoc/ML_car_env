import pygame

from car import Car
from obstacle import Obstacle
from scene import Scene
from utils.constants import *


class Environment(object):
    def __init__(self, size=[640, 480]):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Car parking simulator")
        self.scene = Scene(self.screen)
        self.scene.add_actor(Car())
        self.scene.add_actor(Obstacle(1))
        self.scene.add_actor(Obstacle(2))
        self.scene.add_actor(Obstacle(4))
        pygame.mouse.set_visible(0)

    def step(self, action_value):
        self.scene.update(Action(action_value))

    def render(self):
        self.screen.fill(WHITE)
        self.scene.draw()
        pygame.display.flip()