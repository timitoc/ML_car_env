import numpy as np
import pygame

from car import Car
from obstacle import Obstacle
from parking_spot import ParkingSpot
from scene import Scene
from utils.constants import *
from utils.point import Point
from random import randint

obstacle_images = []
obstacle_images.append('obstacle0.png')
obstacle_images.append('obstacle1.png')
obstacle_images.append('obstacle2.png')

class Environment(object):
    def __init__(self, size=[720, 420], enable_rendering=True):
        self.current_frame = 0
        self.size = size
        self.enable_rendering = enable_rendering
        self.initial_distance = None
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        if enable_rendering:
            pygame.display.set_caption("Car parking simulator")
            self.scene = Scene(self.screen, self.size)
        else:
            self.scene = Scene(None, self.size)
        self.reset()
        # pygame.mouse.set_visible(0)

    def step(self, action_value):
        self.scene.update(Action(action_value))
        observation = self.scene.get_observation()
        reward = self.scene.get_reward(self.initial_distance, self.current_frame)
        done = self.scene.check_done(self.current_frame)
        info = self.scene.get_auxiliar_info()
        self.current_frame += 1
        # print "Reward ", reward, " on frame ", self.current_frame
        # print observation
        return observation, reward, done, info

    def reset(self):
        self.scene.clear()
        # self.scene.add_park(ParkingSpot(Point(350, 340)))
        # self.scene.set_car(Car())
        # self.scene.add_obstacle(Obstacle(Point(25, 350)))
        # self.scene.add_obstacle(Obstacle(Point(200, 350)))
        # self.scene.add_obstacle(Obstacle(Point(600, 350)))
        self.random_car_fixed_obstacles_scenario()

        # self.initial_distance = self.scene.get_distance_to_goal()
        self.initial_distance = INITIAL_DISTANCE_BENCH
        self.current_frame = 0
        return self.scene.get_observation()

    def random_car_fixed_obstacles_scenario(self):
        self.scene.add_park(ParkingSpot(Point(350, 340)))
        car_x_limit = 600
        car_y_limit = 200
        self.scene.set_car(Car((int(car_x_limit * np.random.random_sample()),
                                int(car_y_limit * np.random.random_sample()))))
        self.scene.add_obstacle(Obstacle(Point(25, 350), obstacle_images[randint(0, 2)]))
        self.scene.add_obstacle(Obstacle(Point(200, 350), obstacle_images[randint(0, 2)]))
        self.scene.add_obstacle(Obstacle(Point(600, 350), obstacle_images[randint(0, 2)]))

        self.scene.add_obstacle(Obstacle(Point(-2, 0), 'obstacle_width.png'))
        self.scene.add_obstacle(Obstacle(Point(720, 0), 'obstacle_width.png'))
        self.scene.add_obstacle(Obstacle(Point(0, -2), 'obstacle_length.png'))
        self.scene.add_obstacle(Obstacle(Point(0, 420), 'obstacle_length.png'))

    def render(self):
        if not self.enable_rendering:
            return
        self.screen.fill(WHITE)
        self.scene.draw()
        pygame.display.flip()
