"""
Day 14, Task 2 -- Python: convert integers to and from any base (2..36).

THE PROBLEM
------------
Implement two functions WITHOUT using int(s, base) or format()/bin()/hex():

    to_base(n, base)    -> str   digits are 0-9 then a-z (lowercase);
                                 negative numbers get a leading '-';
                                 to_base(0, b) == "0"
    from_base(s, base)  -> int   accepts upper or lower case digits and
                                 an optional leading '-'

    to_base(255, 16)   -> "ff"
    to_base(-10, 2)    -> "-1010"
    from_base("Zz", 36) -> 1295

Raise ValueError when the base is outside 2..36, when s is empty (or
just "-"), or when a character is not a valid digit for that base.

HOW TO WORK THROUGH THIS
-------------------------
to_base: repeated divmod(n, base), collect remainders, reverse.
from_base: Horner's rule: value = value * base + digit.

Run: python3 base_convert.py
"""

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n: int, base: int) -> str:
    if not isinstance(base, int) or base < 2 or base > 36:
        raise ValueError("base must be in 2..36")
    if n == 0:
        return "0"
    neg = n < 0
    n = -n if neg else n
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(DIGITS[r])
    if neg:
        out.append("-")
    return "".join(reversed(out))


def from_base(s: str, base: int) -> int:
    if not isinstance(base, int) or base < 2 or base > 36:
        raise ValueError("base must be in 2..36")
    neg = s.startswith("-")
    body = s[1:] if neg else s
    if not body:
        raise ValueError("no digits")
    value = 0
    for ch in body.lower():
        d = DIGITS.find(ch)
        if d < 0 or d >= base:
            raise ValueError(f"invalid digit {ch!r} for base {base}")
        value = value * base + d
    return -value if neg else value


def _run_tests() -> None:
    assert to_base(0, 2) == "0"
    assert to_base(255, 16) == "ff"
    assert to_base(-10, 2) == "-1010"
    assert to_base(1295, 36) == "zz"
    assert to_base(8, 8) == "10"
    assert from_base("ff", 16) == 255
    assert from_base("FF", 16) == 255
    assert from_base("-1010", 2) == -10
    assert from_base("Zz", 36) == 1295
    assert from_base("0", 7) == 0
    for bad in [("", 10), ("-", 10), ("12", 2), ("g", 16), ("1", 1), ("1", 37)]:
        try:
            from_base(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")
    for base in (1, 37):
        try:
            to_base(5, base)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for bad base")
    import random
    random.seed(14)
    for _ in range(300):
        n = random.randint(-10**9, 10**9)
        b = random.randint(2, 36)
        assert from_base(to_base(n, b), b) == n, (n, b)
        assert int(to_base(n, b), b) == n, (n, b)
    print("All base_convert tests passed.")


if __name__ == "__main__":
    _run_tests()
