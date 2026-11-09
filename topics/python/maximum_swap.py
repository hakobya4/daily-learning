"""
Day 48, Task 1 -- Python: maximum value after at most one digit swap.

THE PROBLEM
------------
Given a non-negative integer num, you may swap two of its digits at most once.
maximum_swap(num) returns the largest number you can obtain.
Examples: 2736 -> 7236, 9973 -> 9973 (already maximal), 98368 -> 98863, 1993 -> 9913.
Hint: record the LAST index of each digit 0-9; scan left to right and, for each
position, look for a larger digit (9 down to digit+1) that occurs later.

Run: python3 maximum_swap.py
"""


def maximum_swap(num):
    digits = list(str(num))
    last = {int(d): i for i, d in enumerate(digits)}
    for i, d in enumerate(digits):
        for bigger in range(9, int(d), -1):
            j = last.get(bigger, -1)
            if j > i:
                digits[i], digits[j] = digits[j], digits[i]
                return int("".join(digits))
    return num


def _run_tests():
    assert maximum_swap(2736) == 7236
    assert maximum_swap(9973) == 9973
    assert maximum_swap(0) == 0
    assert maximum_swap(1) == 1
    assert maximum_swap(10) == 10
    assert maximum_swap(98368) == 98863
    assert maximum_swap(1993) == 9913
    assert maximum_swap(115) == 511
    assert maximum_swap(12) == 21
    assert maximum_swap(1000000) == 1000000
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
