# We're not going to use floats, sqrt, or atan2; it can all be done with integers.
# However we will need some elementary vector algebra:
gcd = lambda a, b: gcd(b, a % b) if b else abs(a) # no math.gcd() in Python 2.7
norm = lambda (x, y): scalarDivision((x, y), gcd(x, y))
dotProduct = lambda (a, b), (c, d): (a * c, b * d) # not using numpy's, I guess
translation = lambda (a, b), (c, d): (a + c, b + d)
scalarDivision = lambda (a, b), k: (a // k, b // k) # k is never 0 in context
squaredEuclidean = lambda (x, y): x**2 + y**2

from itertools import product
def solution(dimensions, shooter, target, distance):

    # We unfold the billiard into its corresponding Veech surface.
    # This billiard is a rectangle, so its Veech surface is of genus 1,
    # which means it is made up of 4 mirror images:
    W, H = (2 * dimensions[0], 2 * dimensions[1])
    images = lambda (x, y): ((x, y), (W - x, y), (x, H - y), (W - x, H - y))
    friendlies, targets = images(shooter), images(target)

    # Everything we want to compute in this problem depends on the shooter's position:
    recenter = lambda (x, y): (x - shooter[0], y - shooter[1])
    normalize = lambda v: norm(recenter(v)) if v != shooter else (0, 0)
    M = lambda v: squaredEuclidean(recenter(v))

    # Tiling the plane with the Veech surface and enumerating the resulting bogeys:
    boundX, boundY = 2 + distance // W, 2 + distance // H
    bogeys = ((translation(dotProduct(T, (W, H)), bogey), bogey in targets)
            for bogey in friendlies + targets
            for T in product(xrange(-boundX, boundX), xrange(-boundY, boundY)))

    seen = {}
    limit = distance**2 # sqrt(x^2 + y^2) <= D <=> x^2 + y^2 <= D^2
    trajectories = ((normalize(v), M(v), isHostile) for v, isHostile in bogeys)
    for angle, metric, isHostile in trajectories:
        if metric <= limit and (angle not in seen or seen[angle][0] > metric):
            seen[angle] = (metric, isHostile)

    return len([angle for angle, (_, isHostile) in seen.items() if isHostile])

# Probably like half of the execution time of this program is spent raveling and
# unraveling call stacks for a dozen lambdas, all of which could very easily be
# inlined by the interpreter, but aren't. Such is the pythonic way of life.

# I = ((3,2), (1,1), (2,1), 4) # 7, 0.06s
# I = ((3,2), (2,1), (1,1), 100) # 3995, 0.09s
# I = ((3,2), (2,1), (1,1), 500) # 99463, 0.92s
# I = ((300, 275), (150, 150), (180, 100), 500) # 9, 0.06s
# I = ((300, 275), (150, 150), (180, 100), 0) # 0, 0.06s
# I = ((1250, 1250), (1000, 1000), (500, 400), 10000) # 196, 0.06s
# S = solution(*I)
# print(S)
