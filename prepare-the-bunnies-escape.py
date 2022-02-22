# -*- coding: utf-8 -*-
# Let us define two sets of vertices I and O, and a norm over their intersection:
#   I is the set of vertices reachable from source,
#   O is the set of vertices reachable from sink, and
#   ‖X‖ = distance(source, X) + distance(X, sink)
# We know that if removing a single wall w from the map creates a
# path from the entrance to the exit, then that path is of length ‖w‖.
# Problem statement: we want to find X ∈ I⋂O such that:
#   ∀Y ∈ I⋂O ‖X‖ <= ‖Y‖
# With two breadth-first searches we compute I, O, and ‖v‖, ∀v ∈ I⋂O.
# We can then find the smallest ‖v‖ in O(n) time and return it.

from itertools import product
from collections import deque


def solution(matrix):
    w, h = len(matrix), len(matrix[0])
    source, sink = (0, 0), (w - 1, h - 1)
    G = {(x, y): matrix[x][y] for x, y in product(xrange(w), xrange(h))}

    def wall(v):
        return G[v] == 1

    def shortestPaths(G, source, sink):
        Q, S = deque([(source, 0)]), {source: 0}

        def neighbors(x, y):
            return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}

        while Q:
            v, d = Q.popleft()
            moves = (neighbors(*v) & G.viewkeys()) - S.viewkeys()
            S.update({u: d + 1 for u in moves})
            Q.extend((u, d + 1) for u in moves if not wall(u) and u != sink)
        return S

    I, O = shortestPaths(G, source, sink), shortestPaths(G, sink, source)
    candidates = (v for v in I.viewkeys() & O.viewkeys() if wall(v) or v == source)

    def norm(v):
        return I[v] + O[v]

    best = min(candidates, key=norm)
    return norm(best) + 1
