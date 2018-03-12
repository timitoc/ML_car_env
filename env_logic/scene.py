from cmath import sqrt

from pygame import Rect

from utils.constants import TIME_STEP_PENALTY
from utils.point import Point


class Scene:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.actors = []
        self.car = None
        self.parking_spots = []
        self.obstacles = []

    def draw(self):
        for actor in self.actors:
            actor.draw(self.screen)

    def add_actor(self, actor):
        self.actors.append(actor)

    def set_car(self, car):
        self.car = car
        self.add_actor(car)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)
        self.add_actor(obstacle)

    def add_park(self, parking_spot):
        self.parking_spots.append(parking_spot)
        self.add_actor(parking_spot)

    def clear(self):
        self.car = None
        self.obstacles = []
        self.actors = []

    def update(self, action):
        for actor in self.actors:
            actor.update(action)

    def get_distance_to_goal(self):
        x, y, w, h = self.car.rect
        car_center = Point(x + w / 2, y + h / 2)
        x, y, w, h = self.parking_spots[0].rect
        park_center = Point(x + w / 2, y + h / 2)
        return car_center.distance_to(park_center)

    def get_observation(self):
        return []

    def get_reward(self, initial_distance):
        return TIME_STEP_PENALTY + (initial_distance - self.get_distance_to_goal()) / initial_distance

    def check_done(self):
        for obstacle in self.obstacles:
            if self.car.obstacle_check(obstacle) is not None:
                return True
        if self.car.border_check(self.size):
            return True
        return False

    def get_auxiliar_info(self):
        return {}
