# Problem statement:
    # We have an array of digits. We want to find the biggest multiple of 3 that it's
    # possible to make by juxtaposing some or all the digits in the array, in any order.

# We know that:
    # A number is divisible by 3 if and only if the sum of its digits is divisible by 3.
    # If p is divisible by 3, then so are all of p + 0, p + 3, p + 6, and p + 9.
    # The biggest number with k digits is smaller than the smallest k+1 digit number.
    # Addition is commutative, i.e. if we have a multiple of 3 then all
    # possible rearrangements of its digits are also multiples of 3.
    # For a given set S of digits, the biggest number we can make using the digits in S
    # will have its digits in decreasing order.
        # (e.g. for S = {1 2 3}, we have 123 < 132 < 213 < 231 < 312 < 321)

# Therefore, the solution will have the following characteristics:
    # Its digits will be in decreasing order.
    # It will feature all the digits in the array that are multiples of 3 (0, 3, 6, 9);
    # combined with as many digits as possible that sum to a multiple of 3.

# Refined problem statement:
    # We have a multiset P such that ∀x ∈ P, x ≢ 0 mod 3
    # We want to find Q ⊆ P of smallest sum and cardinality such that:
    # sum(P - Q) ≡ 0 mod 3

from itertools import combinations
from functools import reduce
def solution(L):

    def list2num(L):
        """Takes a list of digits and returns the corresponding number,
        e.g. list2num([1,2,3]) = 123"""
        return reduce(lambda a, b: 10 * a + b, L, 0)

    excess = sum(L) % 3
    P = sorted(n for n in L if n % 3)

    for cardinality in range(0, len(P) + 1):
    # We start with a set of cardinality 0, i.e. the empty set {∅},
    # in case L already sums to a multiple of 3 and we don't need to
    # remove anything.

        for Q in combinations(P, cardinality):
            # itertools.combinations emits items in lexicographic order,
            # so, because we sorted P, we know that the smallest candidate Qs
            # will come first, and we are therefore guaranteed to find first
            # the smallest Q that fits our constraints.

            if sum(Q) % 3 == excess:
            # There is a slight inefficiency here in that if P contains duplicates
            # then certain values of Q might be evaluated multiple times. We can't
            # use a set because Python sets don't preserve order, and the language
            # does not provide an ordered set data structure. We could store past
            # values in a set and perform an O(1) membership test before summing,
            # but it's not worth managing an entire extra data structure here, since
            # len(L) is small and we'll at most have a handful of small subsets.

                for q in Q: L.remove(q)
                # Similarly here, it is a tad suboptimal to perform len(Q) removals
                # when list.remove() runs in O(n) time, however going back and forth
                # between the input List L and collections.Counter objects for P and Q
                # (which would let us remove Q from L in O(len(Q)) time) would
                # complexify the code a lot and not result in any appreciable
                # performance benefit under the present constraints.

                L.sort(reverse=True)
                return list2num(L)
