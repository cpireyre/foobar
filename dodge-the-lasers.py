from decimal import Decimal as D
from decimal import ROUND_DOWN, getcontext

def solution(str_n):
    getcontext().prec=200
    getcontext().rounding=ROUND_DOWN
    alpha = D(2).sqrt()
    beta = 2 + alpha

    def recur(n):
        if n <= 1:
            return n
        else:
            N = D(n * alpha).to_integral()
            m = D(N / beta).to_integral()
            return (N**2 + N) / 2 - m**2 - m - recur(m)

    ret = recur(int(str_n))
    return format(int(ret), "d")
