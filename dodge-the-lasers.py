# coding: utf-8
# Let α = √2 and B(α, n) = ⌊α⌋, ⌊2⋅α⌋, ⌊3⋅α⌋, ... ⌊n⋅α⌋ its partial Beatty sequence.
# Let N = ⌊n⋅α⌋.

# α is irrational, therefore, by the Rayleigh–Beatty theorem, there exists
# β = 2 + √2 and m = N / β such that B(α, n) and B(β, m) form a partition
# of the natural numbers from 1 to N.

# We now have: sum(1, ..., N) = sum(B(α, n)) + sum(B(β, m))
# With some arithmetic it is possible to show:
#   sum(B(β, m)) = m(m + 1) + sum(B(α, m))
#   ⇒ sum(B(α, n)) = N(N + 1) / 2 - m(m + 1) - sum(B(α, m))

# We have obtained a recurrence relation allowing us to compute the
# sum of B(α, n) purely in terms of itself and some constant factors.
# Furthermore, because we multiply the index by α/β between steps,
# we have at most a maximum of log β/α (10^100) ≈ 261 steps, which is fine.

# What follows is a relatively straightforward implementation of the recurrence
# relation shown above. A couple implementation details of note:
#   we use decimal.Decimal to obtain arbitrarily precise approximations of α and β,
#   we define rounding = ROUND_DOWN so that .to_integral(x) = ⌊x⌋, and,
#   oddly enough, Decimal objects behave nicely with str(), so no need for format().

from decimal import Decimal, ROUND_DOWN, getcontext


def solution(str_n):
    getcontext().prec = 201
    getcontext().rounding = ROUND_DOWN

    alpha = Decimal(2).sqrt()
    beta = 2 + alpha

    def rayleigh_beatty_sum(n):
        if n <= 1:
            return n
        else:
            N = Decimal(n * alpha).to_integral()
            m = Decimal(N / beta).to_integral()
            return (N**2 + N) / 2 - m**2 - m - rayleigh_beatty_sum(m)

    S = rayleigh_beatty_sum(Decimal(str_n))
    return str(S)
