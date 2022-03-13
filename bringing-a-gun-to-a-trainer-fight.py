# all the coprime translations of alpha by (W * x, H * y), x, y in Z
# with norm less than D
# minus the ones with smaller period than D?
# just gen everyone and compute with gcd
# unless you were multiples with (W, 0), (0, H) or (W, H)
# i.e. everyone where W | x or H | y
# and only need to test half of them because???
from pprint import pprint

# |T| = sqrt(ax**2 + W**2 x**2 + ay**2 +  H**2 y**2)
# ax^2 + W^2 x^2 + ay^2 + H^2 y^2 < D^2
# W^2 x^2 + H^2 y^2 < D^2 - ax^2 - ay^2
from itertools import product


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def sign(x):
    return 1 if x > 0 else -1


from math import atan2, hypot
def solution(dimensions, shooter, target, distance):
    W, H = dimensions
    shooterx, shootery = shooter
    boundx, boundy = 50, 50

    def M(x, y):
        # return hypot(x - shooterx, y - shootery)
        return (x - shooterx) ** 2 + (y - shootery) ** 2
    distance *= distance

    def norm(x, y):
        # return atan2(x - shooterx, y - shootery)
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
    def translate((Tx, Ty), (x, y)):
        return (2 * W * Tx + x, 2 * Ty * H + y)
    def shoot(T, bogeys, isHostile):
        for b in (translate(T, b) for b in bogeys):
            bnorm, bmetric = norm(*b), M(*b)
            if bmetric <= distance and (bnorm not in A or A[bnorm][0] > bmetric):
                A[bnorm] = (bmetric, isHostile)

    for T in product(range(-boundx, boundx + 1), range(-boundy, boundy + 1)):
        shoot(T, friendlies, False)
        shoot(T, bogeys, True)
    pprint(A)
    return [k for k, v in A.items() if v[1]]


# So = solution((3,2), (1,1), (2,1), 4) # 7
# So = solution((3,2), (2,1), (1,1), 100) # 3995
# So = solution((3,2), (2,1), (1,1), 500) # 99465
So = solution((300, 275), (150, 150), (185, 150), 500) # 9
# pprint(So)
print(len(So))
# import matplotlib.pylab as plt

# matrix = [[0 for _ in range(300)] for _ in range(300)]
# offset = 150
# matrix[offset][offset] = 2
# for x, y in S:
#     matrix[offset + y][offset + x] = 1
# print(len(S))
# plt.spy(matrix, marker=".", markersize=2)
# plt.show()
