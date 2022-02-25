from pprint import pprint
def insert(trie, n):
    divisors = [d for d in trie.viewkeys() - {"end"} if n % d == 0]
    if not divisors:
        trie[n] = {"end": 1}
    else:
        for d in divisors:
            insert(trie[d], n)

from math import factorial
def nchoosek(n, k):
    if n < k:
        return 0
    elif n == k:
        return 1
    else:
        return (factorial(n)) / (factorial(k) * (factorial(n - k)))

def search(trie, n, depth=0):
    divisors = [d for d in trie.viewkeys() - {"end"} if n % d == 0]
    if not divisors:
        return nchoosek(depth, 2)
    else:
        return sum(search(trie[d], n, depth + 1) for d in divisors)

def solution(ns):
    trie = dict()
    acc = 0
    for n in ns:
        s = search(trie, n)
        acc += s
        insert(trie, n)
    return acc

# ns = [1,2,4] # 1
# print(solution(ns))
# ns = [1,1,2] # 1
# print(solution(ns))
# ns = [9,3,9,9] # 2
# print(solution(ns))
# ns = [1,1,1] # 1
# print(solution(ns))
# ns = [1,1] # 0
# print(solution(ns))
# ns = [1,2,4,8] # 4?
# print(solution(ns))
