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
obstacle_images.append('obstacle3.png')
obstacle_images.append('obstacle4.png')

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

        self.random_vertical_scenario()

        # self.initial_distance = self.scene.get_distance_to_goal()
        self.initial_distance = INITIAL_DISTANCE_BENCH
        self.current_frame = 0
        return self.scene.get_observation()

    def pseudo_random_vertical_scenario(self):
        self.scene.add_park(ParkingSpot(Point(370, 270)))
        car_x_offset = 20
        car_y_offset = 20
        car_x_limit = 570
        car_y_limit = 180
        self.scene.set_car(Car((car_x_offset + int(car_x_limit * np.random.random_sample()),
                                car_y_offset + int(car_y_limit * np.random.random_sample()))))

        self.scene.add_obstacle(Obstacle(Point(20 + randint(-3, 3), 280 + randint(-3, 3)), obstacle_images[randint(0, 2)]))
        self.scene.add_obstacle(Obstacle(Point(110 + randint(-3, 3), 280 + randint(-3, 3)), obstacle_images[randint(0, 2)]))
        self.scene.add_obstacle(Obstacle(Point(200 + randint(-3, 3), 280 + randint(-3, 3)), obstacle_images[randint(0, 2)]))
        self.scene.add_obstacle(Obstacle(Point(290 + randint(-3, 3), 280 + randint(-3, 3)), obstacle_images[randint(0, 2)]))
        self.scene.add_obstacle(Obstacle(Point(470 + randint(-3, 3), 280 + randint(-3, 3)), obstacle_images[randint(0, 2)]))
        self.scene.add_obstacle(Obstacle(Point(560 + randint(-3, 3), 280 + randint(-3, 3)), obstacle_images[randint(0, 2)]))
        self.scene.add_obstacle(Obstacle(Point(640 + randint(-3, 3), 280 + randint(-3, 3)), obstacle_images[randint(0, 2)]))

        self.scene.add_obstacle(Obstacle(Point(-2, 0), 'obstacle_width.png'))
        self.scene.add_obstacle(Obstacle(Point(720, 0), 'obstacle_width.png'))
        self.scene.add_obstacle(Obstacle(Point(0, -2), 'obstacle_length.png'))
        self.scene.add_obstacle(Obstacle(Point(0, 420), 'obstacle_length.png'))

    def spawn_7(self):
        parking_spot_index = randint(3, 6)
        for i in range(0, 7):
            if i == parking_spot_index:
                self.scene.add_park(ParkingSpot(Point(15 + i * 64 + i * 35 - 15, 260)))
            else:
                self.scene.add_obstacle(Obstacle(Point(15 + i * 64 + i * 35 + randint(-3, 3), 270 + randint(-3, 3)),
                                                 obstacle_images[randint(0, 4)]))

    def spawn_8(self):
        parking_spot_index = randint(3, 7)
        for i in range(0, 8):
            if i == parking_spot_index:
                self.scene.add_park(ParkingSpot(Point(15 + i * 64 + i * 25 - 15, 260)))
            else:
                self.scene.add_obstacle(Obstacle(Point(15 + i * 64 + i * 25 + randint(-3, 3), 270 + randint(-3, 3)),
                                                 obstacle_images[randint(0, 4)]))

    def spawn_9(self):
        parking_spot_index = randint(3, 8)
        for i in range(0, 9):
            if i == parking_spot_index:
                self.scene.add_park(ParkingSpot(Point(15 + i * 64 + i * 15 - 15, 260)))
            else:
                self.scene.add_obstacle(Obstacle(Point(15 + i * 64 + i * 15 + randint(-3, 3), 270 + randint(-3, 3)),
                                                 obstacle_images[randint(0, 4)]))

    def random_vertical_scenario(self):
        number_of_spots = randint(7, 9)
        if number_of_spots == 7:
            self.spawn_7()
        elif number_of_spots == 8:
            self.spawn_8()
        else:
            self.spawn_9()

        car_x_offset = 20
        car_y_offset = 20
        car_x_limit = 0
        car_y_limit = 0
        self.scene.set_car(Car((car_x_offset + int(car_x_limit * np.random.random_sample()),
                                car_y_offset + int(car_y_limit * np.random.random_sample()))))

        # self.scene.set_car(Car((car_x_offset + car_x_limit, car_y_offset + car_y_limit)))

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
