# The basic idea is we unfold the billiard into a torus then tile
# the plane (up to a somewhat arbitrary boundary) with that torus
# and compute all the bogeys, then filter with respect to distance
# from origin and unicity of angle (which we check with the gcd
# of the x and y components).

# No floats, no sqrt, no atan2, all integers.
from itertools import product
def solution(dimensions, shooter, target, distance):
    W, H  = dimensions
    torusW, torusH = 2 * W, 2 * H
    boundx, boundy = 2 + distance // torusW, 2 + distance // torusH
    X, Y = xrange(-boundx, boundx), xrange(-boundy, boundy)
    distance *= distance # sqrt(x^2 + y^2) < D <=> x^2 + y^2 < D^2, so don't need floats

    recenter = lambda (x, y): (x - shooter[0], y - shooter[1])
    squaredEuclidean = lambda (x, y): x**2 + y**2
    M = lambda v: squaredEuclidean(recenter(v))
    gcd = lambda a, b: gcd(b, a % b) if b else abs(a) # no math.gcd() in Python 2.7
    scalarDivision = lambda (a, b), k: (a // k, b // k) # k is never 0 in context
    norm = lambda v: scalarDivision(v, gcd(*v))
    normalize = lambda v: (norm(recenter(v)) if v != shooter else (0, 0), M(v))

    def images(x, y):
        """Returns the 4 reflections of (x, y) in the unfolded torus
        corresponding to the rational billiard on the rectangle (W, H)."""
        xoffset, yoffset = W - x, H - y
        return ((x, y), (x + 2 * xoffset, y), (x, y + 2 * yoffset),
            (x + 2 * xoffset, y + 2 * yoffset))

    def translateImages(T, imgs):
        xoffset, yoffset = torusW * T[0], torusH * T[1]
        return ((x + xoffset, y + yoffset) for x, y in imgs)

    A, friendlies, bogeys = dict(), images(*shooter), images(*target)
    def shoot(T, bogeys, isHostile):
        """Adds the new angles to the dict A assuming they are smaller than any
        previously seen for a given trajectory."""
        for angle, metric in map(normalize, translateImages(T, bogeys)):
            if metric <= distance and (angle not in A or A[angle][0] > metric):
                A[angle] = (metric, isHostile)

    for T in product(X, Y):
        shoot(T, friendlies, False)
        shoot(T, bogeys, True)

    return len([angle for angle, (_, hostile) in A.items() if hostile])


So = solution((3,2), (1,1), (2,1), 4) # 7, 0.06s
print(So)
So = solution((3,2), (2,1), (1,1), 100) # 3995, 0.08s
print(So)
So = solution((3,2), (2,1), (1,1), 500) # 99463, 0.67s
print(So)
So = solution((300, 275), (150, 150), (180, 100), 500) # 9, 0.06s
print(So)
So = solution((300, 275), (150, 150), (180, 100), 0) # 0, 0.06s
print(So)
So = solution((1250, 1250), (1000, 1000), (500, 400), 10000) # 196, 0.06s
print(So)
# 0.69s to run all of the above
