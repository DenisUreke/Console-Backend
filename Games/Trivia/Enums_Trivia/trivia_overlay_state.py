import enum

class TriviaOverlayEnum(enum.Enum):
    NONE = "none"                     # No overlay
    DICE_ROLL = "dice_roll"           # Dice rolling overlay
    CHOICE = "choice"                 # Player choice overlay
    QUESTION = "question"             # Question display overlay
    RESULT = "result"                 # Result display overlay
    PAUSE_MENU = "pause_menu"         # Pause menu overlay