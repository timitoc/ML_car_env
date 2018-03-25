import pygame

from actor import Actor
from utils.point import Point


class ParkingSpot(Actor):
    def __init__(self, position):
        super(ParkingSpot, self).__init__(position, 'park.png')
        self.rect.x = position.x
        self.rect.y = position.y
        self.pivots = []
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super(ParkingSpot, self).draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def set_pivots(self, car_width, car_height):
        cx, cy = self.get_actual_center().to_tuple()
        self.pivots = [Point(cx - car_width / 2, cy - car_height / 2), Point(cx + car_width / 2, cy - car_height / 2),
                       Point(cx + car_width / 2, cy + car_height / 2), Point(cx - car_width / 2, cy + car_height / 2)]
