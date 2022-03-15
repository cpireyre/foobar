def gcd(a, b):  # no math.gcd() in Python 2.7 for some reason
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

    # Tiling the plane with translations of the images from the Veech surface:
    wall, ceiling = 2 + distance // W, 2 + distance // H
    bogeys = (
        ((x + W * Tx, y + H * Ty), (x, y) in targets)
        for (x, y), Tx, Ty in product(
            friendlies + targets, xrange(-wall, wall), xrange(-ceiling, ceiling)
        )
    )

    # Computing distance and bearing of all bogeys relative to the original shooter:
    def bearing(x, y):
        if (x, y) == shooter:
            return (0, 0)
        x, y = x - shooter[0], y - shooter[1]
        g = gcd(x, y)
        return (x // g, y // g)

    def M(x, y):
        return (x - shooter[0]) ** 2 + (y - shooter[1]) ** 2

    limit = distance**2  # sqrt(x^2 + y^2) < D <=> M(x, y) < D^2
    trajectories = (
        (bearing(*v), (M(*v), isTarget)) for v, isTarget in bogeys if M(*v) <= limit
    )

    # Finally, we merge collinear trajectories to single shots, keeping the shortest:
    shots = {}
    for angle, measure in trajectories:
        if angle not in shots or measure < shots[angle]:
            shots[angle] = measure

    return sum(isTarget for _, isTarget in shots.values())


# I = ((3,2), (1,1), (2,1), 4) # 7, 0.06s
# I = ((3,2), (2,1), (1,1), 100) # 3995, 0.08s
# I = ((300, 275), (150, 150), (180, 100), 500) # 9, 0.06s
# I = ((300, 275), (150, 150), (180, 100), 0) # 0, 0.06s
# I = ((1250, 1250), (1000, 1000), (500, 400), 10000) # 196, 0.06s
# I = ((3,2), (2,1), (1,1), 500) # 99463, 0.59s
I = ((3, 2), (2, 1), (1, 1), 1000)  # 397845, 2.43s
S = solution(*I)
print(S)
