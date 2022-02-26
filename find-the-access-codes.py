# Build the transitive closure of // over the input as a bitarray
# then sum all the descendents one level deep for each vertex starting from 0
# resulting matrix is not square exactly, or need not be, because you know in advance the ith vertex can only have len(G)-i edges going out of it
# so, if you can bake offsets into the graph logic, it allows you to pack the representation even further
# it's also unimportant to store the edge from a vertex to itself
# you end up with something kind of in between an adjacency list and adjacency matrix
# except no bitarrays cuz not allowed

from pprint import pprint
from array import array
from itertools import combinations

def solution(s):
    # need V-1 bitarrays with each 1 bit shorter than the last, starting at V-1?
    numVertices = len(s)
    G = list(array('H') for _ in xrange(numVertices))
    for u, v in combinations(xrange(numVertices), 2):
        if not s[v] % s[u]:
            G[u].append(v)

    def luckies(G, v):
        return sum(len(G[u]) for u in G[v])

    return sum(luckies(G, v) for v in xrange(numVertices))

# s = [1] * 2000
# S = solution(s)
# print(S)
# python find-the-access-codes.py  0.36s user 0.02s system 94% cpu 0.403 total

s = [1,1,2,1,2]
print(solution(s))
