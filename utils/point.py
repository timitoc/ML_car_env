from cmath import sqrt


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def to_tuple(self):
        return self.x, self.y

    def distance_to(self, other):
        return (sqrt((self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y))).real

    def on_segment(self, c1, c2):
        return min(c1.x, c2.x) <= self.x <= max(c1.x, c2.x) \
               and min(c1.y, c2.y) <= self.y <= max(c1.y, c2.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


def get_sp_point(a, b, c):
    x1, y1, x2, y2, x3, y3 = a.x, a.y, b.x, b.y, c.x, c.y
    px, py = x2 - x1, y2 - y1
    dab = px * px + py * py
    u = ((x3 - x1) * px + (y3 - y1) * py) / dab
    x, y = x1 + u * px, y1 + u * py
    return Point(x, y)
