import math

delta_x = math.sqrt(3)/4
delta_y = 3/4

step = lambda x: (math.copysign(1, x-1) + 1) / 2
relative_radius = lambda i: math.floor((math.sqrt(48*i + 6) + 6) / 12)
ring_position = lambda i: i - step(i)*(3*relative_radius(i)**2 - 3*relative_radius(i) +1)

scale_factor = lambda z: 1 / ((2*relative_radius(z) + 1))


def hex_x(k):
    i = ring_position(k)
    l = relative_radius(k)
    if i < 1*l: return 2*l - i
    if i < 2*l: return 3*l - 2*i
    if i < 3*l: return l - i
    if i < 4*l: return -5*l + i
    if i < 5*l: return -9*l + 2*i
    return - 4*l + i


def hex_y(k):
    i = ring_position(k)
    l = relative_radius(k)
    if i < 1*l: return i
    if i < 2*l: return l
    if i < 3*l: return 3*l - i
    if i < 4*l: return 3*l - i
    if i < 5*l: return -l
    return -6*l + i

    