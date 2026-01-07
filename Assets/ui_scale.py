BASE_W, BASE_H = 960, 640

def sx(x, w):  # scale x/width
    return int(x * (w / BASE_W))

def sy(y, h):  # scale y/height
    return int(y * (h / BASE_H))