from itertools import product
from pprint import pprint
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
def sign(x):
    return 1 if x > 0 else -1
def solution(dimensions, shooter, target, distance):
    width, height = dimensions[0], dimensions[1]
    boundx, boundy = 1 + distance // width, 1 + distance // height
    rangex, rangey = range(-boundx, boundx + 1), range(-boundy, boundy + 1)
    (shooterx, shootery), (targetx, targety) = shooter, target
    bx, by = width - targetx, height - targety
    fx, fy = width - shooterx, height - shootery
    alphax, alphay = targetx - shooterx, targety - shootery
    Bx = [x for k in rangex for x in (2*k*width + alphax, 2*k*width + alphax + 2 * bx)]
    By = [y for k in rangex for y in (2*k*height+ alphay, 2*k*height + alphay + 2 * by)]
    Fx = [x for k in rangex for x in (2*k*width, 2*k*width + 2 * fx)]
    Fy = [y for k in rangex for y in (2*k*height, 2*k*height + 2 * fy)]

    def M(x, y):
        return x**2 + y**2

    def norm(x, y):
        if not x and not y:
            return (0, 0)
        xSign, ySign = sign(x), sign(y)
        x, y = abs(x), abs(y)
        divisor = gcd(x, y)
        return (xSign * x // divisor, ySign * y // divisor)

    A = dict()
    distance *= distance
    for f in product(Fx, Fy):
        fnorm, fmetric = norm(*f), M(*f)
        if fmetric <= distance and (fnorm not in A or A[fnorm][0] > fmetric):
            A[fnorm] = (fmetric, False)
    for b in product(Bx, By):
        bnorm, bmetric = norm(*b), M(*b)
        if bmetric <= distance and (bnorm not in A or A[bnorm][0] > bmetric):
            A[bnorm] = (bmetric, True)

    return set(k for k, (m, v) in A.items() if v)
    # return len(list(k for k, (m, v) in A.items() if v))

N, S, E, W = (0, -1), (0, 1), (1, 0), (-1, 0)
NE, NW, SE, SW = (1, -1), (-1, -1), (1, 1), (-1, 1)
reflections = {(0, 0): (N, S, E, W, NE, NW, SE, SW),
        N:(N, S, E, W, NE, NW, SE, SW),
        S:(N, S, E, W, NE, NW, SE, SW),
        E:(N, S, E, W, NE, NW, SE, SW),
        W:(N, S, E, W, NE, NW, SE, SW),
        NE:(N, S, E, W, NE, NW, SE, SW),
        NW:(N, S, E, W, NE, NW, SE, SW),
        SE:(N, S, E, W, NE, NW, SE, SW),
        SW:(N, S, E, W, NE, NW, SE, SW),
        }

from collections import namedtuple
from heapq import heapify, heappop, heappush
from pprint import pprint


def solution2(dimensions, shooter, target, distance):
    width, height = dimensions

    distance *= distance
    shooterx, shootery = shooter[0], shooter[1]
    def M(x, y):
        x, y = x - shooterx, y - shootery
        return x**2 + y**2

    def norm(x, y):
        x, y = x - shooterx, y - shootery
        if not x and not y:
            return (0, 0)
        xSign, ySign = sign(x), sign(y)
        x, y = abs(x), abs(y)
        divisor = gcd(x, y)
        return (xSign * x // divisor, ySign * y // divisor)


    Bogey = namedtuple("Bogey", "metric isHostile direction angle x y xOffset yOffset")

    def bogey(x, y, isHostile, direction=(0, 0)):
        return Bogey(
            M(x, y), isHostile, direction, norm(x, y), x, y, (x, width - x), (y, height - y) 
        )

    shooter = bogey(*shooter, isHostile=False)
    target = bogey(*target, isHostile=True)
    if target.metric > distance:
        return 0

    def reflect(b, horizontal=1, vertical=1):
        nX = b.x + horizontal * 2 * b.xOffset[max(0, horizontal)]
        nY = b.y + vertical * 2 * b.yOffset[max(0, vertical)]
        nXOffset = (b.xOffset[1], b.xOffset[0]) if horizontal else b.xOffset
        nYOffset = (b.yOffset[1], b.yOffset[0]) if vertical else b.yOffset
        return Bogey(
            M(nX, nY), b.isHostile, (horizontal, vertical), norm(nX, nY), nX, nY, nXOffset, nYOffset 
            )

    def neighbors(bogey):
        return (reflect(bogey, *r) for r in reflections[bogey.direction])

    Q = [target, shooter]
    heapify(Q)
    seenHostile = {target.angle}
    seenFriendly = {shooter.angle}
    # pprint(target)
    while Q:
        curr = heappop(Q)
        # print("Reflections of %s, metric %d" % ((curr.x, curr.y),curr.metric))
        for img in neighbors(curr):
            if img.metric <= distance and img.angle not in seenHostile and img.angle not in seenFriendly:
                # pprint(img)
                heappush(Q, img)
                if img.angle in ((65,76),(77,64)):
                    print(img)
                (seenHostile if img.isHostile else seenFriendly).add(img.angle)
    return seenHostile


# S = solution((3,2), (1,1), (2,1), 4) # 7
# pprint(S)

# S = solution((3,2), (1,1), (2,1), 500) 
# Sprime = solution2((3,2), (1,1), (2,1), 500) 
# pprint(Sprime - S)
# pprint(S - Sprime)
# print(len(Sprime))
# print(len(S))
# import matplotlib.pylab as plt
# matrix = [[0 for _ in range(1000)] for _ in range(1000)]
# offset = 500
# matrix[offset][offset] = 2
# for x, y in S:
#     matrix[offset + y][offset + x] = 1
# plt.spy(matrix, marker=".", markersize=2)
# plt.show()

# dimensions = (3, 2)
# me = (1, 1)
# trainer = (2, 1)
# distance = 100
# S = solution(dimensions, me, trainer, distance) # 3995, 0.17s
# print(len(S))

# dimensions = (3, 2)
# me = (1, 1)
# trainer = (2, 1)
# distance = 220
# S = solution(dimensions, me, trainer, distance) # 19265, 0.61s
# print(len(S))
# pprint(S)

# S = solution((3,2), (1,1), (2,1), 500) # 99465, 3.12s
# # assert(S) == 99465
# pprint(S)

# dimensions = (300, 275)
# me = (150, 150)
# trainer = (185, 100)
# distance = 500
# S = solution(dimensions, me, trainer, distance) # 9
# Sprime = solution2(dimensions, me, trainer, distance) # 9
# pprint(S)
# pprint(Sprime)
