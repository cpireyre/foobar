from pprint import pprint
def insert(trie, n):
    divisors = [m for m in trie.viewkeys() - {"end"} if n % m == 0]
    curr = trie.get("end", 0)
    pprint("n = %d, curr = %d" % (n, curr))
    if not divisors:
        trie[n] = {"end": 1}
        return curr
    elif n in divisors:
        trie[n]["end"] += 1
        return curr
    else:
        return curr + sum(insert(trie[d], n) for d in divisors)

from math import factorial
def kchoose2(k):
    return 0 if k < 2 else factorial(k) / 2 * factorial(k - 2)

def solution(ns):
    trie = dict()
    acc = 0
    for n in ns:
        tmp = insert(trie, n)
        print("n = %d, insert = %d" % (n, tmp))
        acc += kchoose2(tmp)
    pprint(trie)
    return acc

# ns = [1,2,4] # 1
# print(solution(ns))
# ns = [1,1,2] # 1
# print(solution(ns))
ns = [1,2,2] # 1
print(solution(ns))
# ns = [1,1,1] # 1
# print(solution(ns))
# ns = [1,1] # 0
# print(solution(ns))
# ns = [1,2,4,8] # 4?
# print(solution(ns))
