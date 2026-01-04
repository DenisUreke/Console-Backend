from dataclasses import dataclass
from typing import Optional

from Games.Trivia.Enums_Trivia.trivia_tile_type import TileType
from Games.Trivia.Enums_Trivia.trivia_categories_enum import WedgeColor, TPWedgeCategory

@dataclass(frozen=True)
class RingTile:
    id: int
    x: int
    y: int
    tile_type: TileType
    color: Optional[WedgeColor] = None
    category: Optional[TPWedgeCategory] = None
    label: Optional[str] = None  # for debugging <--- remove later idiot
    
    

# Ring data in clockwise order (as you extracted it)
RING_RAW = [
    (555, 245, "pink",   "wedge"),
    (694, 185, "blue",   "normal"),
    (798, 153, None,     "roll_again"),
    (910, 139, "orange", "normal"),
    (1024, 142, "yellow","normal"),
    (1139, 157, None,    "roll_again"),
    (1243, 186, "purple","normal"),
    (1385, 248, "green", "wedge"),
    (1514, 341, "purple","normal"),
    (1595, 422, None,    "roll_again"),
    (164,  509, "blue",  "normal"),
    (1719, 608, "pink",  "normal"),
    (1761, 710, None,    "roll_again"),
    (1786, 821, "yellow","normal"),
    (1804, 973, "orange","wedge"),
    (1789, 1129,"yellow","normal"),
    (1761, 1234, None,   "roll_again"),
    (1718, 1337,"purple","normal"),
    (1660, 1436,"green", "normal"),
    (1592, 1523, None,   "roll_again"),
    (1508, 1604,"pink",  "normal"),
    (1385, 1696,"blue",  "wedge"),
    (1242, 1756,"pink",  "normal"),
    (1134, 1788, None,   "roll_again"),
    (1020, 1804,"yellow","normal"),
    (913,  1804,"orange","normal"),
    (804,  1788, None,   "roll_again"),
    (697,  1759,"green", "normal"),
    (558,  1689,"purple","wedge"),
    (425,  1606,"green", "normal"),
    (347,  1529, None,   "roll_again"),
    (275,  1437,"pink",  "normal"),
    (223,  1340,"blue",  "normal"),
    (179,  1235, None,   "roll_again"),
    (147,  1127,"orange","normal"),
    (135,  977, "yellow","wedge"),
    (148,  819, "orange","normal"),
    (180,  708, None,    "roll_again"),
    (216,  604, "green", "normal"),
    (275,  508, "purple","normal"),
    (345,  417, None,    "roll_again"),
    (422,  335, "blue",  "normal"),
]

