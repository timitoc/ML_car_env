import pygame

from actor import Actor
from utils.point import get_sp_point


class Obstacle(Actor):
    def __init__(self, position, spirte_name = ''):
        super(Obstacle, self).__init__(position, spirte_name)
        self.rect.x = position.x
        self.rect.y = position.y
        self.mask = pygame.mask.from_surface(self.image)

    def projection_to(self, point):
        corners = self.get_corners()
        best = float("inf")
        who = point
        for i in range(0, 4):
            c1 = corners[i]
            c2 = corners[(i + 1) % 4]
            candidates = [c1, c2]
            sp = get_sp_point(c1, c2, point)
            if sp.on_segment(c1, c2):
                candidates.append(sp)
            for candidate in candidates:
                if point.distance_to(candidate) < best:
                    best = point.distance_to(candidate)
                    who = candidate
        return who

    def draw(self, screen):
        super(Obstacle, self).draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))
