from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class PossibleMove:
    index: int
    tile_type: str                 # "NORMAL" | "WEDGE" | "ROLL_AGAIN"
    category: Optional[str]        # e.g. "HISTORY" | ... | None

@dataclass(frozen=True)
class PossibleMovesData:
    dice_value: int
    moves: List[PossibleMove]