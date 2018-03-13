import pygame

from car import Car
from obstacle import Obstacle
from parking_spot import ParkingSpot
from scene import Scene
from utils.constants import *
from utils.point import Point


class Environment(object):
    def __init__(self, size=[720, 420], enable_rendering=True):
        self.current_frame = 0
        self.size = size
        self.enable_rendering = enable_rendering
        self.initial_distance = None
        if enable_rendering:
            pygame.init()
            self.screen = pygame.display.set_mode(size)
            pygame.display.set_caption("Car parking simulator")
            self.scene = Scene(self.screen, self.size)
        else:
            self.scene = Scene(None, self.size)
        self.reset()
        # pygame.mouse.set_visible(0)

    def step(self, action_value):
        self.scene.update(Action(action_value))
        observation = self.scene.get_observation()
        reward = self.scene.get_reward(self.initial_distance)
        done = self.scene.check_done(self.current_frame)
        info = self.scene.get_auxiliar_info()
        # print observation
        self.current_frame += 1
        # print "Reward ", reward, " on frame ", self.current_frame
        return observation, reward, done, info

    def reset(self):
        self.scene.clear()
        self.scene.add_park(ParkingSpot(Point(350, 340)))
        self.scene.set_car(Car())
        self.scene.add_obstacle(Obstacle(Point(25, 350)))
        self.scene.add_obstacle(Obstacle(Point(200, 350)))
        self.scene.add_obstacle(Obstacle(Point(600, 350)))
        self.initial_distance = self.scene.get_distance_to_goal()
        self.current_frame = 0
        return self.scene.get_observation()

    def render(self):
        if not self.enable_rendering:
            return
        self.screen.fill(WHITE)
        self.scene.draw()
        pygame.display.flip()
