from itertools import product, permutations, chain, tee


def pairwise(xs):  # itertools.pairwise() was introduced in Python 3.10
    a, b = tee(xs)
    next(b, None)
    return zip(a, b)


def partialPermutations(xs):
    return chain.from_iterable(permutations(xs, r) for r in range(len(xs) + 1))


def solution(G, limit):
    source, sink = 0, len(G) - 1
    V, bunnies = range(sink + 1), range(1, sink)

    # Computing the min cost transitive closure of G with Floyd–Warshall:
    for k, i, j in product(V, V, V):
        G[i][j] = min(G[i][j], G[i][k] + G[k][j])
        if G[i][i] < 0: # if G contains a negative cycle, we can save everyone
            return [bunny - 1 for bunny in bunnies]

    def cost(path):
        return sum(G[u][v] for u, v in pairwise((source,) + path + (sink,)))

    # Checking all paths. Note that permutations() emits in lexicographic order.
    best = ()
    for path in partialPermutations(bunnies):
        if cost(path) <= limit and len(path) > len(best):
            best = path

    return [bunny - 1 for bunny in sorted(best)]
