"""
Day 61, Task 7 -- CS fundamentals: big-number multiplication on digit strings (schoolbook vs. Karatsuba).

THE PROBLEM
------------
Pretend Python has no big integers: numbers are non-negative DECIMAL STRINGS like
"12345678901234567890". You may convert only SMALL pieces (at most 9 digits) to int
while computing; never call int() on a whole input, never use str(int * int) on
anything longer than 9 digits per factor. (The tests compare against Python ints.)

1) add_str(a, b) -> str          digit-wise addition with carry
2) sub_str(a, b) -> str          a - b, assuming a >= b (result >= 0)
3) schoolbook_mul(a, b) -> str   the O(n*m) grade-school algorithm
4) karatsuba_mul(a, b) -> str    Karatsuba, O(n^1.585):
     split both numbers at m = max(len(a), len(b)) // 2 digits FROM THE RIGHT:
        a = a1 * 10^m + a0,   b = b1 * 10^m + b0
     z2 = a1*b1,  z0 = a0*b0,  z1 = (a1+a0)*(b1+b0) - z2 - z0
     result = z2 * 10^(2m) + z1 * 10^m + z0   (multiplying by 10^k = appending k zeros)
   Recurse until either operand is shorter than THRESHOLD digits, then fall back to
   schoolbook_mul.

All results must be NORMALISED: no leading zeros, and zero is "0". Inputs may contain
leading zeros ("007") and must still work. Inputs are non-empty strings of 0-9 only;
raise ValueError otherwise.

Finally, karatsuba_mul of two 3000-digit numbers must be noticeably faster than
schoolbook_mul (the test asserts at least 1.5x) -- if it isn't, check that you are not
copying/stripping strings excessively and that THRESHOLD is sensible (16..64).

Hint: work on reversed lists of ints internally for add/sub/schoolbook, and only
convert to/from strings at the boundaries.

Run: python3 karatsuba_bigmul.py
"""

THRESHOLD = 32


_DIGITS = frozenset("0123456789")


def _check(*nums):
    for x in nums:
        if not isinstance(x, str) or not x or not set(x) <= _DIGITS:
            raise ValueError("not a non-negative decimal string: %r" % (x,))


def _to_digits(s):
    """Decimal string -> little-endian list of ints, leading zeros stripped ([] for 0)."""
    d = [ord(c) - 48 for c in reversed(s)]
    while d and d[-1] == 0:
        d.pop()
    return d


def _to_str(d):
    while d and d[-1] == 0:
        d.pop()
    return "".join(chr(48 + x) for x in reversed(d)) if d else "0"


def _add(x, y):
    if len(x) < len(y):
        x, y = y, x
    out = []
    carry = 0
    for i in range(len(x)):
        s = x[i] + (y[i] if i < len(y) else 0) + carry
        if s >= 10:
            out.append(s - 10)
            carry = 1
        else:
            out.append(s)
            carry = 0
    if carry:
        out.append(1)
    return out


def _sub(x, y):
    """x - y for little-endian digit lists with x >= y."""
    out = []
    borrow = 0
    for i in range(len(x)):
        s = x[i] - (y[i] if i < len(y) else 0) - borrow
        if s < 0:
            out.append(s + 10)
            borrow = 1
        else:
            out.append(s)
            borrow = 0
    if borrow:
        raise ValueError("sub_str requires a >= b")
    while out and out[-1] == 0:
        out.pop()
    return out


def _school(x, y):
    if not x or not y:
        return []
    res = [0] * (len(x) + len(y))
    for i, xi in enumerate(x):
        if xi == 0:
            continue
        carry = 0
        k = i
        for yj in y:
            t = res[k] + xi * yj + carry
            carry, res[k] = divmod(t, 10)
            k += 1
        while carry:
            t = res[k] + carry
            carry, res[k] = divmod(t, 10)
            k += 1
    while res and res[-1] == 0:
        res.pop()
    return res


def _shift(x, k):
    return [0] * k + x if x else []


def _kara(x, y):
    if len(x) < THRESHOLD or len(y) < THRESHOLD:
        return _school(x, y)
    m = max(len(x), len(y)) // 2
    x0, x1 = x[:m], x[m:]
    y0, y1 = y[:m], y[m:]
    while x0 and x0[-1] == 0:
        x0.pop()
    while y0 and y0[-1] == 0:
        y0.pop()
    z2 = _kara(x1, y1)
    z0 = _kara(x0, y0)
    z1 = _sub(_sub(_kara(_add(x1, x0), _add(y1, y0)), z2), z0)
    res = _add(_add(_shift(z2, 2 * m), _shift(z1, m)), z0)
    while res and res[-1] == 0:
        res.pop()
    return res


def add_str(a, b):
    _check(a, b)
    return _to_str(_add(_to_digits(a), _to_digits(b)))


def sub_str(a, b):
    _check(a, b)
    return _to_str(_sub(_to_digits(a), _to_digits(b)))


def schoolbook_mul(a, b):
    _check(a, b)
    return _to_str(_school(_to_digits(a), _to_digits(b)))


def karatsuba_mul(a, b):
    _check(a, b)
    return _to_str(_kara(_to_digits(a), _to_digits(b)))


def _run_tests():
    import random
    import sys
    import time

    if hasattr(sys, "set_int_max_str_digits"):   # Python 3.11+ caps str<->int at 4300 digits
        sys.set_int_max_str_digits(0)

    assert add_str("999", "1") == "1000"
    assert add_str("0", "0") == "0"
    assert add_str("007", "3") == "10"
    assert sub_str("1000", "1") == "999"
    assert sub_str("5", "5") == "0"
    assert sub_str("100000000000000000000", "99999999999999999999") == "1"
    assert schoolbook_mul("12", "34") == "408"
    assert schoolbook_mul("0", "123456") == "0"
    assert schoolbook_mul("000", "0001") == "0"
    assert karatsuba_mul("1234", "5678") == "7006652"
    assert karatsuba_mul("0", "0") == "0"
    assert karatsuba_mul("1", "0000000000000000000000000000000000000000001") == "1"
    for bad in ("", "12a", "-5", " 1"):
        for f in (add_str, sub_str, schoolbook_mul, karatsuba_mul):
            try:
                f(bad, "1")
            except ValueError:
                pass
            else:
                raise AssertionError("expected ValueError for %r in %s" % (bad, f.__name__))

    rng = random.Random(61)

    def rnd(k):
        return "".join(rng.choice("0123456789") for _ in range(k))

    for _ in range(400):
        a, b = rnd(rng.randint(1, 120)), rnd(rng.randint(1, 120))
        ia, ib = int(a), int(b)
        assert add_str(a, b) == str(ia + ib)
        hi, lo = (a, b) if ia >= ib else (b, a)
        assert sub_str(hi, lo) == str(abs(ia - ib))
        assert schoolbook_mul(a, b) == str(ia * ib)
        assert karatsuba_mul(a, b) == str(ia * ib), (a, b)
    # very unbalanced lengths
    a, b = rnd(500), rnd(3)
    assert karatsuba_mul(a, b) == str(int(a) * int(b))
    assert karatsuba_mul("9" * 257, "9" * 129) == str((10 ** 257 - 1) * (10 ** 129 - 1))

    a, b = "1" + rnd(2999), "1" + rnd(2999)
    t0 = time.perf_counter()
    s1 = schoolbook_mul(a, b)
    t1 = time.perf_counter()
    s2 = karatsuba_mul(a, b)
    t2 = time.perf_counter()
    assert s1 == s2 == str(int(a) * int(b))
    assert (t1 - t0) > 1.5 * (t2 - t1), "karatsuba %.3fs vs schoolbook %.3fs" % (t2 - t1, t1 - t0)
    print("all tests passed (schoolbook %.2fs, karatsuba %.2fs)" % (t1 - t0, t2 - t1))


if __name__ == "__main__":
    _run_tests()
