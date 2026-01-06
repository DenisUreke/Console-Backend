from enum import Enum
from Games.Trivia.Models.trivia_models import TriviaCategory

class TPPhase(Enum):                # waiting for players / ready state
    TURN_START = "turn_start"       # set active player, prep UI
    AWAIT_ROLL = "await_roll"       # phone shows "Roll"
    CHOOSE_MOVE = "choose_move"     # Choose location to move to
    MOVING = "moving"               # token/camera movement is happening
    AWAIT_DECISION = "await_decision"  # CW/CCW or enter-center choice (generic decision gate)
    QUESTION = "question"           # question overlay active
    RESULT = "result"               # result overlay active
    TURN_END = "turn_end"           # cleanup, advance player
    GAME_OVER = "game_over"         # someone won
    PAUSED = "paused"               # game is paused
    TRIVIA_LOBBY = "trivia_lobby"  # trivia lobby overlay active

