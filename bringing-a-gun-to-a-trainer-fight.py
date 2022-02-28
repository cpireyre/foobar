# Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

# The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000

from math import sqrt
from itertools import product
def solution(dimensions, your_position, trainer_position, distance):

    wall, ceiling = dimensions[0] - 1, dimensions[1] - 1
    def show(dimensions, *args):
        x, y = dimensions
        arena = [['.' for _ in xrange(x)] for _ in xrange(y)]
        for i, (a, b) in enumerate(args):
            arena[b][a] = chr(i + ord('A'))
        return '\n'.join(' '.join(row) for row in arena)

    def norm(v):
        x, y = v
        return sqrt(x*x + y*y)

    def distance(u, v):
        return abs(norm(u) - norm(v))

    def project(origin, direction):
        x, y = direction
        boundary_x = wall if x > 0 else 0 if x < 0 else 2**31
        boundary_y = ceiling if y > 0 else 0 if y < 0 else 2**31
        coef_x = distance((origin[0], 0), (boundary_x, 0))
        coef_y = distance((0, origin[1]), (0, boundary_y))
        coef = int(min(coef_x, coef_y))
        return (origin[0] + x * coef, origin[1] + y * coef)

    shots = list(set(product([-1, 0, 1], [-1, 0, 1])) - {(0, 0)})
    print(shots)
    impacts = [project(your_position, shot) for shot in shots]
    display = show(dimensions, your_position, trainer_position,
            impacts[0],
            impacts[1],
            impacts[2],
            impacts[3],
            impacts[4],
            impacts[5],
            impacts[6],
            impacts[7]
            )
    return display

dimensions = (10, 10)
trainer = (2, 1)
me = (1, 4)
distance = 10

S = solution(dimensions, me, trainer, distance)
print(S)
