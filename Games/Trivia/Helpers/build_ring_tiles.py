from typing import List, Optional
from dataclasses import dataclass
from Games.Trivia.Enums_Trivia.trivia_tile_type import TileType
from Games.Trivia.Enums_Trivia.trivia_categories_enum import WedgeColor, TPWedgeCategory, COLOR_TO_WEDGE_CATEGORY
from Games.Trivia.Models.trivia_game_models import RingTile, RING_RAW


def build_ring_tiles() -> List[RingTile]:
    tiles: List[RingTile] = []
    ring_raw = RING_RAW

    for i, (x, y, color_name, kind) in enumerate(ring_raw):
        if kind == "roll_again":
            tiles.append(RingTile(
                id=i,
                x=x,
                y=y,
                tile_type=TileType.ROLL_AGAIN,
                color=None,
                category=None,
                label="roll again"
            ))
            continue

        # normal or wedge
        if color_name is None:
            raise ValueError(f"Tile {i} is {kind} but has no color_name")

        color = WedgeColor(color_name.lower())
        category = COLOR_TO_WEDGE_CATEGORY[color]
        tile_type = TileType.WEDGE if kind == "wedge" else TileType.NORMAL

        tiles.append(RingTile(
            id=i,
            x=x,
            y=y,
            tile_type=tile_type,
            color=color,
            category=category,
            label=f"{color.value} {kind}"
        ))

    return tiles
