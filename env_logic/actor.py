from utils.point import Point


class Actor(object):
    def __init__(self, position=Point(0, 0)):
        self.name = "ok"
        self.position = position

    def draw(self, screen):
        pass
        # print ("Attempt to draw " + self.name)

    def update(self, action):
        pass

