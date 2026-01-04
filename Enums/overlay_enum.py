from enum import Enum

class OverlayState(Enum):
    NONE = "none"
    TRIVIA_DICE_ROLL = "dice_roll"
    TRIVIA_CHOICE = "choice"
    TRIVIA_QUESTION = "question"
    TRIVIA_RESULT = "result"
    TRIVIA_PAUSE_MENU = "pause_menu"
