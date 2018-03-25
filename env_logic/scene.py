from cmath import log

import pygame

from utils.constants import *
from utils.point import Point, convert_to_polar


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
        # for corner in self.car.get_corners():
        #    self.debug_circle(self.closest_obstacle(corner))
        for corner in self.car.get_corners():
            self.debug_circle(corner)
        for g in self.parking_spots[0].pivots:
            self.debug_circle(g)

    def debug_circle(self, point):
        pygame.draw.circle(self.screen, BLACK, (int(point.x), int(point.y)), 5)

    def add_actor(self, actor):
        self.actors.append(actor)

    def set_car(self, car):
        self.car = car
        _, _, w, h = self.car.rect
        self.parking_spots[0].set_pivots(w, h)
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
        car_center = self.car.get_actual_center()
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
        [8], [9]: float, float -> vector from lower right corner to closest obstacle
        [10], [11]: float, float -> vector from lower left corner to closest obstacle
        [12], [13]: float, float -> vector from car center to goal center
    """

    def get_observation(self):
        import math
        closely = []
        for corner in self.car.get_corners():
            closely.append(corner - self.closest_obstacle(corner))
        car_center = self.car.get_actual_center()
        to_goal = car_center - self.parking_spots[0].get_actual_center()

        if OBS_POLAR:
            closely, to_goal = convert_to_polar(closely), convert_to_polar(to_goal)
            new_arr = []
            for close in closely:
                new_arr.append(Point(float(close.x) / INITIAL_DISTANCE_BENCH, float(close.y) / math.pi))
            closely = new_arr
            to_goal = Point(to_goal.x / INITIAL_DISTANCE_BENCH, to_goal.y / math.pi)
        else:
            new_arr = []
            for close in closely:
                new_arr.append(Point(float(close.x) / self.size[0], float(close.y) / self.size[1]))
            closely = new_arr
            to_goal = Point(to_goal.x / self.size[0], to_goal.y / self.size[1])

        return [float(self.car.angle) / 360,
                float(self.car.speed) / 6,
                # float(car_center.x) / self.size[0], float(car_center.y) / self.size[1],
                closely[0].x, closely[0].y,
                closely[1].x, closely[1].y,
                closely[2].x, closely[2].y,
                closely[3].x, closely[3].y,
                to_goal.x, to_goal.y
                ]

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

    @staticmethod
    def dist_reward_function(actual_distance, initial_distance):
        basic = -log(max(actual_distance / initial_distance, 0.000045)).real
        # if basic > 1:
        #     basic = basic * basic
        return basic

    def corner_style_reward(self, initial_distance, current_frame):
        distance_rew = 0
        corner_dists = []
        if self.car_reached_goal():
            distance_rew = GOAL_REWARD
        else:
            car_corners = self.car.get_corners()
            park_corners = self.parking_spots[0].pivots
            for i in range(0, 4):
                corner_dists.append(car_corners[i].distance_to(park_corners[i]))
                # distance_rew += self.dist_reward_function(corner_dists[i], initial_distance)
            distance_rew = min([self.dist_reward_function(corner_dist, initial_distance)
                                for corner_dist in corner_dists]) + \
                           sum([self.dist_reward_function(corner_dist, initial_distance)
                                for corner_dist in corner_dists]) / 6

        return distance_rew

    def get_reward(self, initial_distance, current_frame):
        if self.car_hit_obstacle():
            return HIT_PENALTY
        if current_frame >= FRAME_LIMIT:
            return FORFEIT_PENALTY

        return self.corner_style_reward(initial_distance, current_frame)

        if self.car_reached_goal():
            distance_rew = GOAL_REWARD
        else:
            distance_rew = self.dist_reward_function(self.get_distance_to_goal(), initial_distance)
            # distance_rew = ((initial_distance - self.get_distance_to_goal()) / initial_distance + 1) ** 5 - 1
        # print self.car.angle, " ", -log(float(self.car.angle)/360 + 0.001).real

        import math
        if self.get_distance_to_goal() < 45.0:
            angle_closure = 1.0 * (self.car.angle if self.car.angle < 180 else 360 - self.car.angle)
            angle_def = 1 - angle_closure / 180.0
            angle_def = 1
            angle_rew = max(distance_rew * angle_def * angle_def, self.dist_reward_function(45.0, initial_distance))
            if angle_closure < 90:
                angle_rew += math.cos(math.radians(angle_closure)).real
        else:
            angle_rew = distance_rew
        return angle_rew
        # return TIME_STEP_PENALTY + 1.0/5 * (initial_distance - self.get_distance_to_goal()) / initial_distance

    def car_hit_obstacle(self):
        for obstacle in self.obstacles:
            if self.car.obstacle_check(obstacle) is not None:
                return True
        if self.car.border_check(self.size):
            return True

    def car_reached_goal(self):
        goal_point = self.parking_spots[0].get_actual_center()
        car_point = self.car.get_actual_center()
        distance_left = car_point.distance_to(goal_point)
        # print distance_left
        good_angle = (340 < self.car.angle < 360 or 0 < self.car.angle < 20)
        return distance_left < GOAL_DISTANCE_MARGIN and good_angle

    def check_done(self, current_frame):
        if self.car_hit_obstacle():
            return True
        # if self.car_reached_goal():
        #     return True
        if current_frame >= FRAME_LIMIT:
            return True
        return False

    def get_auxiliar_info(self):
        return {}
