import pygame
import math

from actor import Actor
from utils.constants import *
from utils.point import Point, rotate


def sgn(number):
    if number < 0:
        return -1
    return 1


class Car(Actor):
    def __init__(self, position=(0, 0)):
        super(Car, self).__init__(position, 'car.png')
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.realcentx, self.realcenty = self.rect.centerx + position[0], self.rect.centery + position[1]
        self.turn_speed = 0.4
        self.angle = 0.0
        self.speed = 0.0
        self.mask = pygame.mask.from_surface(self.image)
        self.rotate_spr()

    def get_corners(self):
        cx, cy = self.get_actual_center().to_tuple()
        _, _, w, h = self.original_image.get_rect()
        simple_corners = [Point(cx - w / 2, cy - h / 2), Point(cx + w / 2, cy - h / 2),
                          Point(cx + w / 2, cy + h / 2), Point(cx - w / 2, cy + h / 2)]
        return rotate(simple_corners, Point(cx, cy), -math.radians(self.angle))

    def rotate_spr(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        oldcenx, oldceny = self.realcentx, self.realcenty
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = oldcenx, oldceny
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super(Car, self).draw(screen)
        self.rotate_spr()
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def border_check(self, bounds):
        x, y, w, h = self.rect
        center_x, center_y = x + w / 2, y + h / 2
        return center_x < 32 or center_x > bounds[0] - 32 or center_y < 64 or center_y > bounds[1] - 64

    def obstacle_check(self, obstacle):
        return pygame.sprite.collide_mask(self, obstacle)

    def parked_check(self, parking_spot):
        collision_mask = pygame.sprite.collide_mask(self, parking_spot)
        return collision_mask and self.realcenter.distance_to(parking_spot.get_actual_center()) < 10 \
               and self.angle < 20 and self.angle > 340

    def update(self, action):
        if action == Action.STEER_LEFT:
            self.angle += (self.turn_speed * self.speed)
        elif action == Action.STEER_RIGHT:
            self.angle -= (self.turn_speed * self.speed)
        elif action == Action.ACCELERATE:
            if self.speed < 4:
                self.speed += 0.4
        elif action == Action.REVERSE:
            if self.speed > -4:
                self.speed -= 0.4

        elif action == Action.BREAK:
            if self.speed != 0:
                self.speed += (-0.8 * sgn(self.speed))
        elif action == Action.ACCELERATE_RIGHT:
            if self.speed <= 4:
                self.speed += 0.4
            self.angle -= (self.turn_speed * self.speed)
        elif action == Action.ACCELERATE_LEFT:
            if self.speed <= 4:
                self.speed += 0.4
            self.angle += (self.turn_speed * self.speed)
        if math.fabs(self.speed) < 0.4:
            self.speed = 0

        self.angle %= 360

        angle_in_rad = math.radians(float(self.angle))

        cos_of_angle = math.cos(angle_in_rad)
        sin_of_angle = math.sin(angle_in_rad)

        to_move_x = self.speed * cos_of_angle
        to_move_y = self.speed * sin_of_angle

        self.realcentx += to_move_x
        self.realcenty -= to_move_y
