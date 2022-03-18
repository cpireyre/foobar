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


def pairwise(xs):  # itertools.pairwise() was introduced in Python 3.10
    a, b = tee(xs)
    next(b, None)
    return zip(a, b)


def partialPermutations(xs):
    return chain.from_iterable(permutations(xs, r) for r in range(len(xs) + 1))


def solution(G, limit):
    source, sink = 0, len(G) - 1
    V, bunnies = xrange(len(G)), xrange(1, sink)
    for k, i, j in product(V, V, V):
        G[i][j] = min(G[i][j], G[i][k] + G[k][j])
        if G[i][i] < 0:
            return [bunny - 1 for bunny in bunnies]

    def cost(path):
        return sum(G[u][v] for u, v in pairwise((source,) + path + (sink,)))

    best = ()
    for path in partialPermutations(bunnies):
        if cost(path) <= limit:
            best = path if len(path) > len(best) else min(best, path)
    return [bunny - 1 for bunny in sorted(best)]


# times, time = [
#     [0, 2, 2, 2, -1],
#     [9, 0, 2, 2, -1],
#     [9, 3, 0, 2, -1],
#     [9, 3, 2, 0, -1],
#     [9, 3, 2, 2, 0],
# ], 1  # [1, 2]
# times, time = [[-20, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], -1000 # [0, 1, 2]
times, time = [
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0],
], 3  # [0, 1]
# times, time = [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 100 # [0, 1, 2], 0.05s
# times, time = [[0, 1], [1, 0]], 10 # []
# times, time = [[-10, 1], [1, 0]], 10 # []
# times, time = [[2, 1], [1, 0]], -30 # []
S = solution(times, time)
print(S)
