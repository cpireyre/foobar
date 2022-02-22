# We have an array P of peg positions.
# Per the problem statement there are k pegs, 2 <= k <= 20.

# Let us define P(i) as the position of the i-th peg.
# We know i < i + 1 <=> P(i) < P(i + 1) (P is strictly increasing)

# We can now define D as the set of distances between pegs:
    # D(i) = P(i + 1) - P(i) > 0, i <= k - 1

# We also have G, the set of gears, where G(i) is the radius of
# the gear around the i-th peg P(i).

# We want to find G such that, for all i:
    # G(i) + G(i + 1) = D(i)
    # G(i) >= 1
    # G(0) = 2 * G(k)

# Notice that the above implies D(i) - D(i + 1) = G(i) - G(i + 2)
# Therefore:
    # for 0 <= i <= k - 1: sum((-1)^i * D(i)) = G(k) * (2 + (-1)^(k - 1))
    # thus G(k) = sum((-1)^i * D(i)) / (2 + (-1)^(k - 1)) for 0 <= i <= k - 1

from fractions import Fraction
def solution(pegs):

    k = len(pegs) - 1
    D = [right - left for left, right in zip(pegs, pegs[1:])]
    G0 = 2 * Fraction(sum((-1)**i * d for i, d in enumerate(D)), 
            2 + (-1)**(k - 1))

    # We have our prospective solution, now to check if the
    # system of equations is coherent, that is, if the gear radii
    # we derive from Gk all fit the constraint.

    Gi = G0
    for Di in D:
        Gi = Di - Gi
        if Gi < 1:
            return [-1, -1]

    return [G0.numerator, G0.denominator]
