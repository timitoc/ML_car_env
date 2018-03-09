class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.actors = []

    def draw(self):
        for actor in self.actors:
            actor.draw(self.screen)

    def add_actor(self, actor):
        self.actors.append(actor)

    def update(self, action):
        for actor in self.actors:
            actor.update(action)
