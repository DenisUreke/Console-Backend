from enum import Enum, IntEnum

class TileType(str, Enum):
    NORMAL = "normal"         # ask question in tile’s category
    WEDGE = "wedge"           # if correct: award wedge
    ROLL_AGAIN = "roll_again" # special effect, no question

class StartingLocations(IntEnum):
    PINK = 0
    GREEN = 7
    ORANGE = 14
    BLUE = 21
    PURPLE = 28
    YELLOW = 35