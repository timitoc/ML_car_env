import pygame

from actor import Actor

class ParkingSpot(Actor):
    def __init__(self, position):
        self.image = pygame.image.load('sprites/park.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super(ParkingSpot, self).draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))