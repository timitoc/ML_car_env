import pygame

from utils.constants import *
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
        # VISUAL DEBUG
        # closest = self.closest_obstacle(self.car.get_actual_center())
        # self.debug_circle(closest)
        for corner in self.car.get_corners():
            self.debug_circle(corner)

    def debug_circle(self, point):
        pygame.draw.circle(self.screen, GREEN, (int(point.x), int(point.y)), 5)

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

    """
        Returns an array describing the state as:
        [0]: float -> car angle
        [1]: float -> car speed
        [2], [3]: float, float -> car x, y position
        [4], [5]: float, float -> vector from upper left corner to closest obstacle
        [6], [7]: float, float -> vector from upper right corner to closest obstacle
        [8], [9]: float, float -> vector from lower left corner to closest obstacle
        [10], [11]: float, float -> vector from lower right corner to closest obstacle
        [12], [13]: float, float -> vector from car center to goal center
    """

    def get_observation(self):
        return [self.car.angle,
                self.car.speed,
                self.car.get_actual_center().x, self.car.get_actual_center().y]

    """
        Returns a vector(as a point) towards the point from an obstacle closest to the source
    """

    def closest_obstacle(self, source):
        best = float("inf")
        who = source
        for obstacle in self.obstacles:
            project = obstacle.projection_to(source)
            if source.distance_to(project) < best:
                best = source.distance_to(project)
                who = project
        return who

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
