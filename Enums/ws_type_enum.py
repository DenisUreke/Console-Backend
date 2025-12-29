from enum import IntEnum

class WsType(IntEnum):
    # C2S
    HELLO = 10
    INPUT = 20

    # S2C
    WELCOME = 11
    STATE_GLOBAL = 31
    STATE_PERSONAL = 32
    ANIMATION = 40
    FX = 41
    ERROR = 90
