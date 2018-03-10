import pygame
import math

from actor import Actor
from utils.constants import *
from utils.point import Point


class Car(Actor):
    def __init__(self, position=Point(320, 240)):
        super(Car, self).__init__(position)
        self.image = pygame.image.load('sprites/car.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.turn_speed = 1
        self.angle = 0
        self.speed = 0

    def rotate_spr(self):
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def draw(self, screen):
        super(Car, self).draw(screen)
        self.rotate_spr()
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, action):
        if action == Action.STEER_LEFT:
            self.angle += (self.turn_speed * self.speed) % 360
        elif action == Action.STEER_RIGHT:
            self.angle -= (self.turn_speed * self.speed) % 360
        elif action == Action.ACCELERATE:
            if self.speed <= 5:
                self.speed += 1
        elif action == Action.REVERSE:
            if self.speed >= -3:
                self.speed -= 1
        elif action == Action.BREAK:
            self.speed = 0
        elif action == Action.ACCELERATE_RIGHT:
            if self.speed <= 5:
                self.speed += 1
            self.angle -= (self.turn_speed * self.speed) % 360
        elif action == Action.ACCELERATE_LEFT:
            if self.speed <= 5:
                self.speed += 1
            self.angle += (self.turn_speed * self.speed) % 360

        angle_in_rad = math.radians(self.angle)
        self.rect.x += (self.speed * math.cos(angle_in_rad))
        self.rect.y -= (self.speed * math.sin(angle_in_rad))
