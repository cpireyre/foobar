# The key to this problem is the fact that if M > F, we have:
# (M, F) == (Fq + r, F) where q and r are the quotient and remainder
# of the integer division of M by F.

# Let us define the predecessor configuration of (M, F) as pred(M, F):
    # pred(M, F) == pred(Fq + r, F) -> (Fq + r - F, F)
# Repeating this operation k times with k such that Fq - Fk + r < F yields:
    # (M', F) with F = M'q' + r' => (M', F) == (M', M'q' + r')

# It is becoming apparent that we are reproducing the steps of Euclid's
# algorithm to compute the Greatest Common Divisor of M and F.
# This implies a canonical ancestor of (M, F) -> (0, gcd(M, F))

# The successor of (0, gcd(M, F)) is (gcd(M, F), gcd(M, F))
# Therefore, it is possible to reach (M, F) from (1, 1) if and
# only if M and F are coprime.

# The following algorithm implements this reasoning while keeping
# track of how many generations get walked back at each iteration
# (what was called k, above.)

def solution(x, y):
    def retrace(x, y, generations=0):
        if (x, y) < (1, 1):
            return (x, y, generations)
        if x < y:
            x, y = y, x
        return retrace(x % y, y, generations + x / y)

    M, F, generations = retrace(int(x), int(y))
    return str(generations - 1) if (M, F) == (0, 1) else "impossible"
