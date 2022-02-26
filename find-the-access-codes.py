# coding: utf-8
# Let I be a 0-indexed array of N strictly positive integers.
# We define the divisibility relation over I as follows:
#    "a divides b" or "a | b" iff there exists k in ℕ such that b = a * k
# It is easy to prove that | is transitive:
#   a | b => b = a * k
#   b | c => c = b * k'
#   therefore c = a * k * k', i.e. a divides c.
# Let us define the set of lucky triplets L:
#   L = {(i, j, k) ∈ ⟦0, N - 1⟧³, i < j < k such that I[i] | I[j] | I[k]}
# Problem statement: What is the cardinality of L?

# We represent the transitive closure of | over I as a graph G, constructed
#   in O(n²) time, specifically an adjacency list.
# Thus, for n ∈ I, we can obtain in O(1) time a list M of neighbors of n:
#   that is, all m ∈ I such that n | m.
# We can then fan out and query the lists of neighbors of all m ∈ M.
# Putting these things together allows us to list all the lucky triplets
# of I which begin with n, since:
#   ∀m ∈ M: n | m
#   ∀p ∈ neighbors(m): m | p
#   Therefore all triplets of the form (n, m, p) are lucky, and,
# by the definition of transitive closure, they form a complete list
# of all such triplets.

# We find the final answer by integrating this calculation over all n ∈ I:

def solution(I):
    vertices = range(len(I))
    G = [[v for v in vertices[u + 1 :] if I[v] % I[u] == 0] for u in vertices]

    def neighbors(v):
        return G[v]

    def luckies(v):
        return sum(len(neighbors(u)) for u in neighbors(v))

    return sum(luckies(v) for v in vertices)

# Note: we can achieve a ~30% speedup on the above code by manually inlining
# the calls to luckies() and neighbors(), which CPython will not do. They can
# be folded into the return statement like so:
#   return sum(sum(len(G[u]) for u in G[v]) for v in vertices)
# I chose to make them explicit for the sake of readability as is the Python way,
# given that the program runs fast enough even in the worst case scenario of
# I = [1] * 2000, in which every vertex is connected to every subsequent vertex.
