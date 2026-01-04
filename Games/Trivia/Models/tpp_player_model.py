from dataclasses import dataclass, field
from typing import Set
from typing import Any
from Games.Trivia.Enums_Trivia.trivia_categories_enum import TPWedgeCategory

@dataclass
class TPPlayerToken:
    x: float
    y: float
    target_x: float
    target_y: float
    moving: bool = False

@dataclass
class TPPlayer:
    player_number: int
    name: str
    color_theme: str
    websocket_id: Any # websocket from the orchestrator's player object

    # Player's token on the board
    player_token: TPPlayerToken = field(default_factory=lambda: TPPlayerToken(0,0,0,0))
    
    # Where the token is (for now: ring only)
    ring_index: int = 0

    # Wedges collected
    wedges: Set[TPWedgeCategory] = field(default_factory=set)

    # Optional stats
    correct_answers: int = 0
    turns_taken: int = 0

    @property
    def has_all_wedges(self) -> bool:
        return len(self.wedges) == 6
