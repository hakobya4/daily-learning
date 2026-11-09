"""
Day 50, Task 1 -- Python: happy number.

THE PROBLEM
------------
is_happy(n) for n >= 1: repeatedly replace n by the sum of the squares of its digits.
n is happy if this process reaches 1, and unhappy if it loops forever in a cycle
that does not contain 1. Return True/False.
Examples: 19 -> True (19 -> 82 -> 68 -> 100 -> 1), 2 -> False.
Hint: track seen values in a set (or use Floyd's tortoise and hare).

Run: python3 happy_number.py
"""


def is_happy(n):
    raise NotImplementedError


def _run_tests():
    assert is_happy(19) is True
    assert is_happy(2) is False
    assert is_happy(1) is True
    assert is_happy(7) is True
    assert is_happy(4) is False
    assert [n for n in range(1, 50) if is_happy(n)] == [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
