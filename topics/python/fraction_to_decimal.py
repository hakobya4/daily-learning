"""
Day 43, Task 2 -- Python: fraction to recurring decimal string.

THE PROBLEM
------------
fraction_to_decimal(numerator, denominator) -> str
Return the decimal expansion as a string. If the fractional part repeats,
wrap the repeating block in parentheses.
  1/2 -> "0.5"     2/1 -> "2"     4/333 -> "0.(012)"     1/6 -> "0.1(6)"
  -50/8 -> "-6.25"   0/5 -> "0"   1/-3 -> "-0.(3)"
Use long division; remember the remainder -> position of each remainder in
a dict to detect where the cycle starts. Do not use floats.
denominator is never 0.

Run: python3 fraction_to_decimal.py
"""


def fraction_to_decimal(numerator, denominator):
    raise NotImplementedError


def _run_tests():
    assert fraction_to_decimal(1, 2) == "0.5"
    assert fraction_to_decimal(2, 1) == "2"
    assert fraction_to_decimal(4, 333) == "0.(012)"
    assert fraction_to_decimal(1, 6) == "0.1(6)"
    assert fraction_to_decimal(-50, 8) == "-6.25"
    assert fraction_to_decimal(0, 5) == "0"
    assert fraction_to_decimal(1, -3) == "-0.(3)"
    assert fraction_to_decimal(-1, -3) == "0.(3)"
    assert fraction_to_decimal(22, 7) == "3.(142857)"
    assert fraction_to_decimal(1, 3) == "0.(3)"
    assert fraction_to_decimal(7, 4) == "1.75"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
