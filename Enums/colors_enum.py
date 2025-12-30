# Enums/colors.py
from enum import Enum

class Colors(str, Enum):
    Cyan     = "#00FFFF"
    Magenta  = "#FF00FF"
    Yellow   = "#FFFF00"
    Red      = "#FF0000"
    Green    = "#00FF00"
    Orange   = "#FF7F00"
    Blue     = "#0000FF"
    Purple   = "#7F00FF"

COLOR_LIST = list(Colors)