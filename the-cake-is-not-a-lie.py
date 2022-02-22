# Problem statement: We want to find the minimum length k such that:
# all substrings of s of the form s[n*k:(n+1)*k] are equal

# The proposed solution here rests on two insights:
# k must be a divisor of the length of the input, or we don't have a partition, and
# we can use the first characters of the input as a reference.

def solution(s):

    # We need to know the length of the input to compute divisors and such:
    size = len(s)
    # len in Python is O(1) but since we use this value multiple times,
    # we'd like to avoid function call overhead, which involves global lookup for
    # the symbol, resolving the appropriate method for the input type, etc.

    # Next, we create a generator which will unroll the divisors of len(s) in
    # increasing order. These are our candidate sequence lengths:
    for seql in (d for d in xrange(1, size//2 + 1) if size % d == 0):
    # Generators are lazy which allows us to quit early if appropriate.
    # xrange instead of range because regular range is not lazy in Python 2.7.

    # The algorithm generating these divisors is a bit naive and inefficient;
    # if len(s) were very large it might be better to compute (the permutations of)
    # its prime factorization or to decrease the lower bound of the xrange
    # to the square root of size and compute the divisors by pairs.
    # (e.g. if we know 2 divides 10 we also know 5 does)

    # For maintainability, it might be best to name these generators and extract them
    # from the for loop statements, however we would pay a performance cost as
    # Python might need to allocate and dereference extra symbols. In this case
    # they are easy enough to extract when necessary, though they do make debugging
    # and introspecting slightly harder.

        # Here, we generate the partition of s in substrings of length seql:
        if all(s[o: o + seql] == s[:seql] for o in xrange(seql, size, seql)):
        # This is the most likely performance bottleneck because, as far as I know,
        # for each substring, Python will allocate an entire new string which will
        # need to be garbage collected later. At least we stop early if a substring
        # is found not to match the reference.
        # It may be faster and more economical to use equally-spaced indices to
        # iterate through all the substrings character by character until one fails.
        # I chose not to do this for the sake of concision and legibility; we might
        # also expect Python's string equality checking to be fast enough to limit
        # the damage.

            # If all the substrings in our partition are equal, we have satisfied
            # the constraints of the problem.
            # We can compute the size of the partition and return it
            return size // seql

    # If we have exhausted the list of divisors without finding a satisfactory
    # partition, the only answer left is the trivial partition whose only element
    # contains the entire input array.
    return 1
