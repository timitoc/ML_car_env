import pygame
import math

from actor import Actor
from utils.constants import *
from utils.point import Point


class Car(Actor):
    def __init__(self, position=Point(320, 240)):
        super(Car, self).__init__(position)
        self.image = pygame.image.load('sprites/car.png')
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.angle = 0
        self.speed = 0

    def updateimg(self):
        x, y = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        super(Car, self).draw(screen)
        self.updateimg()
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, action):
        if action == Action.STEER_LEFT:
            self.angle = (self.angle + 0.2) % 360
        elif action == Action.STEER_RIGHT:
            self.angle = (self.angle - 0.2) % 360
        elif action == Action.ACCELERATE:
            if self.speed <= 10:
                self.speed += 0.2
        elif action == Action.BREAK:
            if self.speed > 0:
                self.speed -= 1
            elif self.speed < 0:
                self.speed += 1
        self.rect.x += (self.speed * math.cos(self.angle * (math.pi / 180)))
        self.rect.y += (self.speed * math.sin(self.angle / (math.pi / 180)))
