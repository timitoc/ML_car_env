import pygame

from actor import Actor


class ParkingSpot(Actor):
    def __init__(self, position, normal_angle=0):
        super(ParkingSpot, self).__init__(position, 'park_green.png')
        self.rect.x = position.x
        self.rect.y = position.y
        self.normal_angle = normal_angle
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super(ParkingSpot, self).draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))
