import enum

class TriviaCameraModeEnum(enum.Enum):
    FOLLOW = "follow"         # Camera follows the active player's token
    TRANSITION = "transition" # Camera transitions to a specific location