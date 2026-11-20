"""
Day 60, Task 1 -- Python: split money by ratios without losing a cent (largest remainder).

THE PROBLEM
------------
Money is stored as an integer number of CENTS. Splitting it by ratios with floats or
plain rounding loses or invents cents ("100 split 3 ways" -> 33 + 33 + 33 = 99).

1) allocate(total_cents, weights) -> list[int]
   Split total_cents across len(weights) buckets proportionally to the integer weights,
   using the LARGEST REMAINDER (Hamilton) method:
     - every bucket first gets floor(total * w / sum(weights));
     - the cents still left over go, one each, to the buckets with the largest
       fractional remainders (total * w mod sum(weights)); ties go to the LOWER index;
     - the result always sums to exactly total_cents.
   A NEGATIVE total is split as if positive and every share is negated
   (allocate(-100, [1, 1, 1]) -> [-34, -33, -33]).
   Use only integer arithmetic (no floats, no Fraction/Decimal needed).
   Raise ValueError if weights is empty, any weight is negative, or all weights are 0.
   A bucket with weight 0 always gets 0.

2) format_cents(cents) -> str
   "$1,234.05" style: thousands separators, always two decimals, a leading "-" before
   the "$" for negative amounts ("-$0.07"), and "$0.00" for zero.

Examples:
  allocate(100, [1, 1, 1])        -> [34, 33, 33]
  allocate(1000, [50, 30, 20])    -> [500, 300, 200]
  allocate(5, [3, 7])             -> [2, 3]     (1.5 -> 1, 3.5 -> 3, then the leftover
                                                 cent goes to index 0 on the 0.5 tie)
  format_cents(123405)            -> "$1,234.05"

Hint: compute base = total * w // s and rem = total * w % s per bucket, then hand out
total - sum(base) extra cents to sorted(range(n), key=lambda i: (-rem[i], i)).

Run: python3 money_allocate.py
"""


def allocate(total_cents, weights):
    weights = list(weights)
    if not weights or any(w < 0 for w in weights) or sum(weights) == 0:
        raise ValueError("weights must be non-empty, non-negative and not all zero")
    sign = -1 if total_cents < 0 else 1
    total = abs(total_cents)
    s = sum(weights)
    base = [total * w // s for w in weights]
    rem = [total * w % s for w in weights]
    left = total - sum(base)
    for i in sorted(range(len(weights)), key=lambda i: (-rem[i], i))[:left]:
        base[i] += 1
    return [sign * b for b in base]


def format_cents(cents):
    sign = "-" if cents < 0 else ""
    dollars, c = divmod(abs(cents), 100)
    return "%s$%s.%02d" % (sign, "{:,}".format(dollars), c)


def _run_tests():
    assert allocate(100, [1, 1, 1]) == [34, 33, 33]
    assert allocate(-100, [1, 1, 1]) == [-34, -33, -33]
    assert allocate(1000, [50, 30, 20]) == [500, 300, 200]
    assert allocate(5, [3, 7]) == [2, 3]
    assert allocate(7, [1, 1, 1, 1]) == [2, 2, 2, 1]
    assert allocate(10, [0, 1, 0, 1]) == [0, 5, 0, 5]
    assert allocate(1, [1, 1, 1]) == [1, 0, 0]
    assert allocate(0, [2, 5]) == [0, 0]
    assert allocate(99, [1]) == [99]
    assert allocate(101, [1, 2, 3, 4]) == [10, 20, 30, 41]
    assert allocate(1, [1, 2]) == [0, 1]
    assert allocate(2, [1, 1, 3]) == [1, 0, 1]  # remainders 2, 2, 1 (of 5): tie -> idx 0
    assert allocate(10 ** 18 + 1, [1, 1]) == [5 * 10 ** 17 + 1, 5 * 10 ** 17]
    # property checks
    import random
    rng = random.Random(60)
    for _ in range(500):
        n = rng.randint(1, 8)
        w = [rng.randint(0, 20) for _ in range(n)]
        if sum(w) == 0:
            w[0] = 1
        t = rng.randint(-10000, 10000)
        out = allocate(t, w)
        assert sum(out) == t, (t, w, out)
        s = sum(w)
        for share, wi in zip(out, w):
            exact = abs(t) * wi / s
            assert abs(abs(share) - exact) < 1, (t, w, out)
            if wi == 0:
                assert share == 0
    for bad in ([], [1, -1], [0, 0]):
        try:
            allocate(100, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))

    assert format_cents(123405) == "$1,234.05"
    assert format_cents(0) == "$0.00"
    assert format_cents(-7) == "-$0.07"
    assert format_cents(5) == "$0.05"
    assert format_cents(100) == "$1.00"
    assert format_cents(99999) == "$999.99"
    assert format_cents(100000) == "$1,000.00"
    assert format_cents(-123456789012) == "-$1,234,567,890.12"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
