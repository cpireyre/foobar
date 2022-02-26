def solution(s):
    vertices = range(len(s))
    G = [[v for v in vertices[u + 1 :] if s[v] % s[u] == 0] for u in vertices]

    def neighbors(v):
        return G[v]

    def luckies(v):
        return sum(len(neighbors(u)) for u in neighbors(v))

    return sum(luckies(v) for v in vertices)


s = [1] * 2000
S = solution(s)
print(S)
# python find-the-access-codes.py  0.36s user 0.02s system 94% cpu 0.403 total
# With sublists: 22709120  peak memory footprint

s = [1, 1, 2, 1, 2]
print(solution(s))
