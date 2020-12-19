import math


def to_camel_case(string_ac_underscores):
    words = [word.capitalize() for word in string_ac_underscores.split('_')]
    return "".join(words)


def euclid_distance(coords_a, coords_b):
    xa, ya = coords_a[0], coords_a[1]
    xb, yb = coords_b[0], coords_b[1]
    return math.sqrt((xa - xb)**2 + (ya - yb)**2)


def manhattan_distance(coords_a, coords_b):
    xa, ya = coords_a[0], coords_a[1]
    xb, yb = coords_b[0], coords_b[1]
    return abs(xa - xb) + abs(ya - yb)
