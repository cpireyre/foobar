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
    shooterx, shootery = shooter
    xalpha, yalpha = shooterx - target[0], shootery - target[1]
    Bx = [x for k in rangex for x in (2 * width * k + 1, 2 * width * k + 3)]
    By = [2 * k for k in rangey]
    Fx = [x for k in rangex for x in (2 * width * k - 2, 2 * width * k)]
    Fy = [2 * k for k in rangey]

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

    return list(k for k, (m, v) in A.items() if v)
    # return len(list(k for k, (m, v) in A.items() if v))

# dimensions = (3, 2)
# me = (1, 1)
# trainer = (2, 1)
# distance = 4
# S = solution(dimensions, me, trainer, distance) # 7
# pprint(S)

S = solution((3,2), (1,1), (2,1), 500) 
pprint(len(S))
import matplotlib.pylab as plt
matrix = [[0 for _ in range(1000)] for _ in range(1000)]
offset = 500
matrix[offset][offset] = 2
for x, y in S:
    matrix[offset + y][offset + x] = 1
plt.spy(matrix, marker=".", markersize=2)
plt.show()

# dimensions = (3, 2)
# me = (1, 1)
# trainer = (2, 1)
# distance = 100
# S = solution(dimensions, me, trainer, distance) # 3995, 0.17s
# pprint(S)

# dimensions = (3, 2)
# me = (1, 1)
# trainer = (2, 1)
# distance = 220
# S = solution(dimensions, me, trainer, distance) # 19265, 0.61s
# pprint(S)

# S = solution((3,2), (1,1), (2,1), 500) # 99465, 3.12s
# # assert(S) == 99465
# pprint(S)

# dimensions = (300, 275)
# me = (150, 150)
# trainer = (185, 100)
# distance = 500
# S = solution(dimensions, me, trainer, distance) # 9
# pprint(S)
