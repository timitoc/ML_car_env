import pygame

from actor import Actor


class ParkingSpot(Actor):
    def __init__(self, position):
        super(ParkingSpot, self).__init__(position, 'park_green.png')
        self.rect.x = position.x
        self.rect.y = position.y
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super(ParkingSpot, self).draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))
