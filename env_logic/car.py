import pygame

from actor import Actor
from utils.constants import *
from utils.point import Point


class Car(Actor):
    def __init__(self, position=Point(0, 0)):
        super(Car, self).__init__(position)

    def draw(self, screen):
        super(Car, self).draw(screen)

        # Head
        pygame.draw.ellipse(screen, BLACK, [1 + self.position.x, self.position.y, 10, 10], 0)

        # Legs
        pygame.draw.line(screen, BLACK, [5 + self.position.x, 17 + self.position.y],
                         [10 + self.position.x, 27 + self.position.y], 2)
        pygame.draw.line(screen, BLACK, [5 + self.position.x, 17 + self.position.y],
                         [self.position.x, 27 + self.position.y], 2)

        # Body
        pygame.draw.line(screen, RED, [5 + self.position.x, 17 + self.position.y],
                         [5 + self.position.x, 7 + self.position.y], 2)

        # Arms
        pygame.draw.line(screen, RED, [5 + self.position.x, 7 + self.position.y],
                         [9 + self.position.x, 17 + self.position.y], 2)
        pygame.draw.line(screen, RED, [5 + self.position.x, 7 + self.position.y],
                         [1 + self.position.x, 17 + self.position.y], 2)

    def update(self, action):
        if action == Action.STEER_LEFT:
            self.position.x -= 1
        elif action == Action.STEER_RIGHT:
            self.position.x += 1
        elif action == Action.ACCELERATE:
            self.position.y -= 1
        elif action == Action.BREAK:
            self.position.y += 1
