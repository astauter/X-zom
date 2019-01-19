import math


def distance_to(x1, x2, y1, y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx ** 2 + dy ** 2)
