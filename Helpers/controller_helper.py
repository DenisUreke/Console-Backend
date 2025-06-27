def interpret_angle(direction) -> str:
    if 75 <= direction <= 105:
        return "up"
    elif 255 <= direction <= 295:
        return "down"
    elif 165 <= direction <= 195:
        return "left"
    elif direction >= 345 or direction <= 15:
        return "right"
    elif 16 <= direction <= 74:
        return "up-right"
    elif 106 <= direction <= 164:
        return "up-left"
    elif 196 <= direction <= 254:
        return "down-left"
    elif 296 <= direction <= 344:
        return "down-right"
    else:
        return "unknown"