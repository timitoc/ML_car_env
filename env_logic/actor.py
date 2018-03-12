import pygame

from utils.point import Point


class Actor(object):
    def __init__(self, position=Point(0, 0), sprite_name=None):
        if sprite_name is not None:
            self.image = pygame.image.load('sprites/' + sprite_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.name = "ok"
        self.position = position

    def get_actual_center(self):
        x, y, w, h = self.rect
        return Point(x + w / 2, y + h / 2)

    # Returns [corner points] in clockwise order from upper left
    def get_corners(self):
        x, y, w, h = self.rect
        cx, cy = x + w / 2, y + h / 2
        return [Point(cx-w/2, cy-h/2), Point(cx+w/2, cy-h/2),
                Point(cx-w/2, cy+h/2), Point(cx+w/2, cy+h/2)]

    def draw(self, screen):
        pass
        # print ("Attempt to draw " + self.name)

    def update(self, action):
        pass

