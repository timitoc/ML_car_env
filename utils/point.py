from cmath import sqrt


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def distance_to(self, other):
        return (sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))).real
