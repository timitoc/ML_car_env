from enum import Enum

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

TIME_STEP_PENALTY = -1
HIT_PENALITY = -5
GOAL_REWARD = 10
GOAL_DISTANCE_MARGIN = 8
FRAME_LIMIT = 350


class Action(Enum):
    NOTHING = 0
    CHANGE_DIRECTION = 1
    STEER_LEFT = 2
    STEER_RIGHT = 3
    ACCELERATE = 4
    BREAK = 5
    ACCELERATE_LEFT = 6
    ACCELERATE_RIGHT = 7
    REVERSE = 8
