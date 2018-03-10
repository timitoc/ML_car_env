import pygame

from actor import Actor


class Obstacle(Actor):
    def __init__(self, index=1):
        self.image = obstacle_sprite
        self.rect = self.image.get_rect()
        self.rect.x = index * 50
        self.rect.y = 400

    def draw(self, screen):
        super(Obstacle, self).draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))
