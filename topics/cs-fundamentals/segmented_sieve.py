"""
Day 60, Task 7 -- CS fundamentals: a segmented Sieve of Eratosthenes for far-away ranges.

THE PROBLEM
------------
A plain sieve up to 10^12 needs a terabyte. A SEGMENTED sieve only needs the base primes
up to sqrt(hi) plus one bytearray of size hi - lo + 1.

1) primes_in_range(lo, hi) -> list[int]
   All primes p with lo <= p <= hi, ascending. 0 and 1 are not prime; lo may be 0 or 1.
   Must handle hi up to 10^12 as long as hi - lo <= 2_000_000.
   Return [] when lo > hi. Raise ValueError when lo < 0 or hi - lo > 2_000_000.
2) count_in_range(lo, hi) -> int   (same rules)
3) max_gap(lo, hi) -> tuple | None
   Among CONSECUTIVE primes p < q both inside [lo, hi], the largest q - p; return
   (gap, p, q) for the FIRST (smallest p) such pair, or None if the range holds fewer
   than two primes.

Do NOT use sympy, gmpy2 or trial division per number (too slow); no Miller-Rabin either
-- the point is the sieve.

Examples:
  primes_in_range(10, 30)  -> [11, 13, 17, 19, 23, 29]
  count_in_range(0, 10**6) -> 78498
  max_gap(1, 100)          -> (8, 89, 97)

Hint: base = simple sieve up to isqrt(hi). For every base prime p, start crossing off
at max(p*p, ceil(lo / p) * p) and step by p inside the segment; mark[0..] corresponds to
lo..hi. Slice assignment (seg[start::p] = bytes(len(range(start, size, p)))) is MUCH
faster in Python than an inner for-loop. Remember to clear 0 and 1 if they are in range.

Run: python3 segmented_sieve.py
"""


def primes_in_range(lo, hi):
    raise NotImplementedError


def count_in_range(lo, hi):
    raise NotImplementedError


def max_gap(lo, hi):
    raise NotImplementedError


def _simple(n):
    if n < 2:
        return []
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            for k in range(i * i, n + 1, i):
                s[k] = False
    return [i for i, b in enumerate(s) if b]


def _run_tests():
    import random
    import time

    assert primes_in_range(10, 30) == [11, 13, 17, 19, 23, 29]
    assert primes_in_range(0, 1) == []
    assert primes_in_range(0, 2) == [2]
    assert primes_in_range(2, 2) == [2]
    assert primes_in_range(14, 16) == []
    assert primes_in_range(30, 10) == []
    assert max_gap(1, 100) == (8, 89, 97)
    assert max_gap(0, 2) is None
    assert max_gap(24, 29) is None
    assert max_gap(2, 3) == (1, 2, 3)

    small = _simple(20000)
    rng = random.Random(60)
    for _ in range(200):
        a = rng.randint(0, 20000)
        b = rng.randint(a, 20000)
        want = [p for p in small if a <= p <= b]
        assert primes_in_range(a, b) == want, (a, b)
        assert count_in_range(a, b) == len(want)

    t0 = time.time()
    assert count_in_range(0, 10 ** 6) == 78498
    assert count_in_range(10 ** 6, 2 * 10 ** 6) == 70435
    assert max_gap(0, 10 ** 6) == (114, 492113, 492227)
    # far away: primes just above 10^12 and 10^11
    assert primes_in_range(10 ** 12, 10 ** 12 + 100) == [1000000000039, 1000000000061,
                                                         1000000000063, 1000000000091]
    assert count_in_range(10 ** 12, 10 ** 12 + 10 ** 6) == 36249
    assert max_gap(10 ** 11, 10 ** 11 + 10 ** 6) == (296, 100000902611, 100000902907)
    elapsed = time.time() - t0
    assert elapsed < 20, "too slow: %.1fs" % elapsed

    for bad in ((-1, 10), (0, 2_000_001), (10, 2_000_011)):
        try:
            primes_in_range(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
