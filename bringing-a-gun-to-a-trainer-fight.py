# The basic idea is we unfold the billiard into a torus then tile
# the plane (up to a somewhat arbitrary boundary) with that torus
# and compute all the bogeys, then filter with respect to distance
# from origin and unicity of angle (which we check with the gcd
# of the x and y components).

# No floats, no sqrt, no atan2, all integers.
from itertools import product
def solution(dimensions, shooter, target, distance):
    W, H = dimensions
    boundx, boundy = 2 + distance // (2 * W), 2 + distance // (2 * H)
    shooterx, shootery = shooter

    def M(x, y):
        """Returns a measure of the distance between (x, y) and the shooter."""
        return (x - shooterx) ** 2 + (y - shootery) ** 2
    distance *= distance # Only using squared distances from now on

    def gcd(a, b): # Not in the math module in Python 2.7 for some reason
        while b:
            a, b = b, a % b
        return a

    sign = lambda x: 1 if x >= 0 else -1
    def norm(x, y):
        """Normalizes a vector to coprime components, with respect
        to the shooter, preserves orientation."""
        if (x, y) == (shooterx, shootery):
            return (0, 0)
        x, y = x - shooterx, y - shootery
        signx, signy = sign(x), sign(y)
        x, y = abs(x), abs(y)
        g = gcd(x, y)
        return (signx * (x // g), signy * (y // g))

    def images(x, y):
        """Returns the 4 reflections of (x, y) in the unfolded torus
        corresponding to the rational billiard on the rectangle (W, H)."""
        xoffset, yoffset = W - x, H - y
        return ((x, y), (x + 2 * xoffset, y), (x, y + 2 * yoffset),
            (x + 2 * xoffset, y + 2 * yoffset))

    A, friendlies, bogeys = dict(), images(*shooter), images(*target)

    # I don't totally like how this function mutates in place an out-of-scope object
    def shoot(T, bogeys, isHostile):
        """Adds the new angles to the dict A assuming they are smaller than any
        previously seen for a given trajectory."""
        xoffset, yoffset = 2 * W * T[0], 2 * H * T[1]
        for b in ((x + xoffset, y + yoffset) for x, y in bogeys):
            angle, bmetric = norm(*b), M(*b)
            if bmetric <= distance and (angle not in A or A[angle][0] > bmetric):
                A[angle] = (bmetric, isHostile)

    for T in product(range(-boundx, boundx), range(-boundy, boundy)):
        shoot(T, friendlies, False)
        shoot(T, bogeys, True)

    return len([k for k, v in A.items() if v[1]])


# So = solution((3,2), (1,1), (2,1), 4) # 7, 0.06s
# So = solution((3,2), (2,1), (1,1), 100) # 3995, 0.08s
# So = solution((3,2), (2,1), (1,1), 500) # 99463, 0.67s
# So = solution((300, 275), (150, 150), (180, 100), 500) # 9, 0.06s
# So = solution((300, 275), (150, 150), (180, 100), 0) # 0, 0.06s
# So = solution((1250, 1250), (1000, 1000), (500, 400), 10000) # 196, 0.06s
# print(So)
