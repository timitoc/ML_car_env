class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.actors = []
        self.car = None
        self.obstacles = []

    def draw(self):
        for actor in self.actors:
            actor.draw(self.screen)

    def add_actor(self, actor):
        self.actors.append(actor)

    def set_car(self, car):
        self.car = car
        self.add_actor(car)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)
        self.add_actor(obstacle)

    def clear(self):
        self.car = None
        self.obstacles = []
        self.actors = []

    def update(self, action):
        for actor in self.actors:
            actor.update(action)

    def get_observation(self):
        return []

    def get_reward(self):
        return 0.0

    def check_done(self):
        if self.car.border_check():
            return True
        return False

    def get_auxiliar_info(self):
        return {}
