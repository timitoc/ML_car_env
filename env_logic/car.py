import pygame
import math

from actor import Actor
from utils.constants import *

class Car(Actor):
    def __init__(self):
        self.image = pygame.image.load('sprites/car.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.turn_speed = 1
        self.angle = 0
        self.speed = 0
        self.mask = pygame.mask.from_surface(self.image)

    def rotate_spr(self):
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super(Car, self).draw(screen)
        self.rotate_spr()
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def border_check(self, bounds):
        x, y, w, h = self.rect
        center_x, center_y = x + w/2, y+h/2
        return center_x < 0 or center_x > bounds[0] or center_y < 0 or center_y > bounds[1]

    def obstacle_check(self, obstacle):
        return pygame.sprite.collide_mask(self, obstacle)

    def parked_check(self, parking_spot):
        collision_mask =  pygame.sprite.collide_mask(self, parking_spot)
        return collision_mask and self.rect.x > 900

    def update(self, action):
        if action == Action.STEER_LEFT:
            self.angle += (self.turn_speed * self.speed) % 360
        elif action == Action.STEER_RIGHT:
            self.angle -= (self.turn_speed * self.speed) % 360
        elif action == Action.ACCELERATE:
            if self.speed < 6:
                self.speed += 2
        elif action == Action.REVERSE:
            if self.speed > -4:
                self.speed -= 2
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
