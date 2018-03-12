import pygame

from actor import Actor

class Obstacle(Actor):
    def __init__(self, position):
        self.image = pygame.image.load('sprites/obstacle.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super(Obstacle, self).draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))
