# Key insight: unfold the room into the plane such that all trajectories become
# straight lines between rooms that are symmetrical with respect to the common
# boundary. Now the max distance of the laser beam corresponds to a circle extending
# from your position. In this circle you have x copies of bogeys and x copies of you.
# Count how many bogeys there are with a clear line of sight and you're done.

# Implementation:
#   we could use the Euclidean norm and do everything with regards to it
# but then we have to worry about floats and square roots and that's annoying and slow.
# So define a metric M((x, y)) = x^2 + y^2. Because both squaring and rooting are
# monotonically increasing on R+ we know that if |v| < d then M(v) < d^2, so it's fine
# to use this metric to judge whether or not we can land a shot.
# Now we need a way to find out if vectors are proportional without dividing by the Euclidean norm. So: divide the coordinates by their GCD. This will let you know in constant time if 2 vectors are proportional without departing from integers.

# Putting it all together: use a priority queue keyed by the fake metric and for a given bogey enqueue all 8 of its reflections minus the ones you've seen before and the ones that are too far away. BFS property + heap invariant will ensure that:
#   the enumeration doesn't miss anyone so you can be sure you have visited all the relevant angles, and
#   if a given angle would hit multiple bogeys, you always see the closest one first

# You need a priority queue i.e. heap which will contain tuples like so:
#   (M((x,y)), (x, y), isBogey) where isBogey is an int and either 0 or 1.
#   (may need to specify what to do if two vectors have same norm but it might be fine)
# The Seen set of already visited angles would contain untagged normalized angle vectors
# I can either increment a counter depending on whether bogey or not or split Seen
# into SeenBogey and SeenMyself then return len(SeenBogey), I'm not sure which option is the best re: simplicity, clarity, concision, performance, etc.

# Will also need: a helper function to push an iterable onto a heap
# a function to compute all 8 reflections of a bogey through the 4 walls + 4 corners

# Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

# The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000




def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
def sign(x):
    return 1 if x > 0 else -1



from collections import namedtuple
from heapq import heapify, heappop, heappush
from pprint import pprint


def solution(dimensions, shooter, target, distance):
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


    Bogey = namedtuple("Bogey", "metric isHostile angle x y xOffset yOffset")

    def bogey(x, y, isHostile):
        return Bogey(
            M(x, y), isHostile, norm(x, y), x, y, (x, width - x), (y, height - y) 
        )

    shooter = bogey(*shooter, isHostile=False)
    target = bogey(*target, isHostile=True)
    if target.metric > distance:
        return 0

    def reflect(horizontal=1, vertical=1):
        def f(b):
            nX = b.x + horizontal * 2 * b.xOffset[max(0, horizontal)]
            nY = b.y + vertical * 2 * b.yOffset[max(0, vertical)]
            nXOffset = (b.xOffset[1], b.xOffset[0]) if horizontal else b.xOffset
            nYOffset = (b.yOffset[1], b.yOffset[0]) if vertical else b.yOffset
            return Bogey(
                M(nX, nY), b.isHostile, norm(nX, nY), nX, nY, nXOffset, nYOffset 
            )

        return f

    N, S = reflect(0, -1), reflect(0, 1)
    E, W = reflect(1, 0), reflect(-1, 0)
    NE, NW = reflect(1, -1), reflect(-1, -1)
    SE, SW = reflect(1, 1), reflect(-1, 1)

    def reflections(b):
        return (N(b), S(b), E(b), W(b), NE(b), NW(b), SE(b), SW(b))

    Q = [target, shooter]
    heapify(Q)
    seenHostile = {target.angle}
    seenFriendly = {shooter.angle}
    # pprint(target)
    while Q:
        curr = heappop(Q)
        # print("Reflections of %s, metric %d" % ((curr.x, curr.y),curr.metric))
        for img in reflections(curr):
            if img.metric <= distance and img.angle not in seenHostile and img.angle not in seenFriendly:
                # pprint(img)
                heappush(Q, img)
                (seenHostile if img.isHostile else seenFriendly).add(img.angle)
    return len(seenHostile)


dimensions = (3, 2)
me = (1, 1)
trainer = (2, 1)
distance = 100
S = solution(dimensions, me, trainer, distance) # 7
pprint(S)

# dimensions = (300, 275)
# me = (150, 150)
# trainer = (185, 100)
# distance = 500
# S = solution(dimensions, me, trainer, distance) # 9
# pprint(S)

# dimensions = (1250, 1250)
# me = (150, 150)
# trainer = (185, 100)
# distance = 10000
# S = solution(dimensions, me, trainer, distance) # 9
# pprint(S)
