import pygame

from car import Car
from scene import Scene
from utils.constants import *


class Environment(object):
    def __init__(self, size=[700, 500], enable_rendering=True):
        self.size = size
        self.enable_rendering = enable_rendering
        if enable_rendering:
            pygame.init()
            self.screen = pygame.display.set_mode(size)
            self.scene = Scene(self.screen)
            pygame.display.set_caption("Car parking simulator")
            pygame.mouse.set_visible(0)
        else:
            self.scene = Scene(None)
        self.scene.add_actor(Car())

    def step(self, action_value):
        self.scene.update(Action(action_value))

    def render(self):
        if not self.enable_rendering:
            return
        self.screen.fill(WHITE)
        self.scene.draw()
        pygame.display.flip()
