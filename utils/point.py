from cmath import sqrt, cos, sin

import collections
from math import atan2

import math


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
    dx = x2 - x1
    dy = y2 - y1
    mag = sqrt(dx * dx + dy * dy).real
    dx /= mag
    dy /= mag
    lamb = (dx * (x3 - x1)) + (dy * (y3 - y1))
    x = (dx * lamb) + x1
    y = (dy * lamb) + y1
    return Point(x, y)


"""
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
"""


def rotate(points, origin, angle):
    if isinstance(points, collections.Sequence):
        rez = []
        for p in points:
            rez.append(rotate(p, origin, angle))
        return rez

    ox, oy = origin.to_tuple()
    px, py = points.to_tuple()

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return Point(qx.real, qy.real)


def convert_to_polar(points):
    if isinstance(points, collections.Sequence):
        rez = []
        for p in points:
            rez.append(convert_to_polar(p))
        return rez
    distance = sqrt(points.x * points.x + points.y * points.y).real
    angle = atan2(points.y, points.x) / math.pi
    return Point(distance, angle)
