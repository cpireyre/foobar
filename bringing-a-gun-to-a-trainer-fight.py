def gcd(a, b): # no math.gcd() in Python 2.7 for some reason
    while b:
        a, b = b, a % b
    return abs(a)

from itertools import product
def solution(dimensions, shooter, target, distance):
    # We unfold the billiard into its corresponding Veech surface.
    # This billiard is a rectangle, so its Veech surface is of genus 1,
    # which means it is made up of 4 mirror images:
    W, H = (2 * dimensions[0], 2 * dimensions[1])
    def images(x, y):
        return ((x, y), (W - x, y), (x, H - y), (W - x, H - y))

    friendlies, targets = images(*shooter), images(*target)

    # Repeatedly translating the bogeys embedded in the Veech surface to tile the plane:
    boundX, boundY = 2 + distance // W, 2 + distance // H
    bogeys = (((x + W * Tx, y + H * Ty), (x, y) in targets)
            for x, y in friendlies + targets
            for Tx, Ty in product(xrange(-boundX, boundX), xrange(-boundY, boundY)))

    # Computing distance and bearing of bogeys relative to the original shooter:
    def bearing(x, y):
        if (x, y) == shooter:
            return (0, 0)
        x, y = x - shooter[0], y - shooter[1]
        g = gcd(x, y)
        return (x // g, y // g)

    def M(x, y):
        return (x - shooter[0])**2 + (y - shooter[1])**2

    trajectories = ((bearing(*v), M(*v), isHostile) for v, isHostile in bogeys)

    # We are now ready to check every angle and keep only the bullseyes:
    seen = {}
    limit = distance**2 # sqrt(x^2 + y^2) < D <=> M(x, y) < D^2
    for angle, metric, isHostile in trajectories:
        if metric <= limit and (angle not in seen or seen[angle][0] > metric):
            seen[angle] = (metric, isHostile)

    return sum(isHostile for _, isHostile in seen.values())

# I = ((3,2), (1,1), (2,1), 4) # 7, 0.06s
# I = ((3,2), (2,1), (1,1), 100) # 3995, 0.08s
# I = ((300, 275), (150, 150), (180, 100), 500) # 9, 0.06s
# I = ((300, 275), (150, 150), (180, 100), 0) # 0, 0.06s
# I = ((1250, 1250), (1000, 1000), (500, 400), 10000) # 196, 0.06s
# I = ((3,2), (2,1), (1,1), 500) # 99463, 0.59s
# I = ((3,2), (2,1), (1,1), 1000) # 397845, 2.38s
I = ((3,2), (2,1), (1,1), 3000) #  3580971, 23.7s
S = solution(*I)
print(S)
