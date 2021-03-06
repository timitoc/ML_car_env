from enum import Enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

TIME_STEP_PENALTY = 0
HIT_PENALTY = -30
FORFEIT_PENALTY = 0
GOAL_REWARD = 30
GOAL_DISTANCE_MARGIN = 8
FRAME_LIMIT = 551
INITIAL_DISTANCE_BENCH = 400

OBS_POLAR = True


class Action(Enum):
    NOTHING = 0
    STEER_LEFT = 1
    STEER_RIGHT = 2
    ACCELERATE = 3
    REVERSE = 4
    BREAK = 5
    CHANGE_DIRECTION = 6
    ACCELERATE_LEFT = 7
    ACCELERATE_RIGHT = 8
