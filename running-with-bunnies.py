# think i got it... it's not hard. use johnson's algorithm (modified bellman-ford)
# (or floyd-warshall)
# to compute min cost for all pairs of vertices. if there is a negative cycle, save
# everyone and exit right away.
# if there are no negative cycles, number your bunnies 1-5, say source = 0 and sink = 6, then:
# a rescue path is a sequence like 0 3 2 4 6 (always 0 then some number of bunnies then 6)
# which means if you gen the set of partial permutations of {1 2 3 4 5} you can list all the possible
# rescue paths. then you pairwise, map cost, reduce +, filter out everyone with cost > time_limit,
# group by len, max, sort, output.
# it's OK to compute all this b/c worst case it's like 100 bellman-fords + about 1000 possible paths
# (actually less but approx. this order of magnitude on both counts)

from itertools import product, permutations, chain, tee

def pairwise(xs): # itertools.pairwise() was introduced in Python 3.10
    """pairwise('ABCDEFG') --> AB BC CD DE EF FG"""
    a, b = tee(xs)
    next(b, None)
    return zip(a, b)

def partialPermutations(xs):
    s = list(xs)
    return chain.from_iterable(permutations(s, r) for r in range(len(s) + 1))

from pprint import pprint
def solution(times, times_limit):
    card = len(times)
    V, bunnies = xrange(card), xrange(1, card - 1)
    for k, i, j in product(V, V, V):
        times[i][j] = min(times[i][j], times[i][k] + times[k][j])
        if times[i][i] < 0:
            return list(bunny - 1 for bunny in bunnies)
    def pathCost(path):
        return sum(times[u][v] for u, v in pairwise((0,) + path + (card - 1,)))
    paths = {p:pathCost(p) for p in partialPermutations(bunnies) if pathCost(p) <= times_limit}
    if not paths:
        return []
    best = max(len(path) for path, cost in paths.items())
    res = sorted([path for path in paths if len(path) == best])[0]
    return [bunny - 1 for bunny in res]

times = [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]]
S = solution(times, 1)
pprint(S)
