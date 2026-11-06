"""
Day 46, Task 3 -- Python: validate a number string by hand (finite-state style).

THE PROBLEM
------------
is_number(s) returns True iff s is a valid decimal number, WITHOUT using
float()/int()/regex. Grammar: optional sign, then digits with an optional
single '.', at least one digit somewhere in the mantissa ("4." and ".5" ok,
"." not), then an optional exponent: 'e' or 'E', optional sign, one or more
digits (no '.'). Surrounding whitespace is NOT allowed.

Run: python3 valid_number.py
"""


def is_number(s):
    i, n = 0, len(s)
    if i < n and s[i] in "+-":
        i += 1
    digits = 0
    while i < n and s[i].isdigit() and s[i] in "0123456789":
        i += 1
        digits += 1
    if i < n and s[i] == ".":
        i += 1
        while i < n and s[i] in "0123456789":
            i += 1
            digits += 1
    if digits == 0:
        return False
    if i < n and s[i] in "eE":
        i += 1
        if i < n and s[i] in "+-":
            i += 1
        exp = 0
        while i < n and s[i] in "0123456789":
            i += 1
            exp += 1
        if exp == 0:
            return False
    return i == n


def _run_tests():
    for good in ["0", "-1", "+3.14", "4.", ".5", "2e10", "-90E3", "3e+7", "6.02e-23", "00"]:
        assert is_number(good), good
    for bad in ["", ".", "e", "e3", "1e", "1e+", "--1", "1.2.3", "1e2.5", "abc", "1 ", " 1", "+", "-.", "95a54e53"]:
        assert not is_number(bad), bad
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
