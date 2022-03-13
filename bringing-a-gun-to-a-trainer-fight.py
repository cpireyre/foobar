from itertools import product


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def sign(x):
    return 1 if x >= 0 else -1


def solution(dimensions, shooter, target, distance):
    W, H = dimensions
    shooterx, shootery = shooter
    boundx, boundy = 2 + distance // W, 2 + distance // H

    distance *= distance
    def M(x, y):
        return (x - shooterx) ** 2 + (y - shootery) ** 2

    def norm(x, y):
        x, y = x - shooterx, y - shootery
        if (x, y) == (0, 0):
            return (0, 0)
        signx, signy = sign(x), sign(y)
        x, y = abs(x), abs(y)
        g = gcd(x, y)
        return (signx * (x // g), signy * (y // g))

    def S(x, y):
        xoffset, yoffset = W - x, H - y
        return (
            (x, y),
            (x + 2 * xoffset, y),
            (x, y + 2 * yoffset),
            (x + 2 * xoffset, y + 2 * yoffset),
        )

    friendlies = S(*shooter)
    bogeys = S(*target)

    A = dict()
    def shoot(T, bogeys, isHostile):
        Tx, Ty = T
        xoffset, yoffset = 2 * W * Tx, 2 * H * Ty
        for b in ((x + xoffset, y + yoffset) for x, y in bogeys):
            bnorm, bmetric = norm(*b), M(*b)
            if bmetric <= distance and (bnorm not in A or A[bnorm][0] > bmetric):
                A[bnorm] = (bmetric, isHostile)

    for T in product(range(-boundx, boundx + 1), range(-boundy, boundy + 1)):
        shoot(T, friendlies, False)
        shoot(T, bogeys, True)
    return len([k for k, v in A.items() if v[1]])


# So = solution((3,2), (1,1), (2,1), 4) # 7
So = solution((3,2), (2,1), (1,1), 100) # 3995
# So = solution((3,2), (2,1), (1,1), 500) # 99465
# So = solution((300, 275), (150, 150), (180, 100), 500) # 9
# So = solution((300, 275), (150, 150), (180, 100), 0) # 0
# So = solution((1250, 1250), (1000, 1000), (500, 400), 10000) # 196
print(So)
# import matplotlib.pylab as plt

# matrix = [[0 for _ in range(300)] for _ in range(300)]
# offset = 150
# matrix[offset][offset] = 2
# for x, y in S:
#     matrix[offset + y][offset + x] = 1
# print(len(S))
# plt.spy(matrix, marker=".", markersize=2)
# plt.show()
