import pygame

from actor import Actor


class ParkingSpot(Actor):
    def __init__(self, position, normal_angle=0, allow_reverse_parking=False):
        super(ParkingSpot, self).__init__(position, 'park.png')
        self.rect.x = position.x
        self.rect.y = position.y
        self.normal_angle = normal_angle
        self.allow_reverse_parking = allow_reverse_parking
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        super(ParkingSpot, self).draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def get_angle_delta(self, car_angle):
        simple = abs(car_angle % 360 - self.normal_angle).real
        if not self.allow_reverse_parking:
            return simple
        rev = abs(car_angle % 360 - ((self.normal_angle + 180) % 360)).real
        return min(simple, rev)

