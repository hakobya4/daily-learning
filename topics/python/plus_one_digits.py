"""
Day 50, Task 2 -- Python: plus one on a digit list.

THE PROBLEM
------------
digits is a non-empty list of decimal digits, most significant first, representing a
non-negative integer with no leading zeros (except the number 0 itself, [0]).
plus_one(digits) returns a NEW list representing that integer plus one. Do not convert
to int/str. Example: [1,2,9] -> [1,3,0], [9,9] -> [1,0,0].
Hint: walk from the right with a carry; handle the all-9s case by prepending 1.

Run: python3 plus_one_digits.py
"""


def plus_one(digits):
    raise NotImplementedError


def _run_tests():
    assert plus_one([1, 2, 3]) == [1, 2, 4]
    assert plus_one([1, 2, 9]) == [1, 3, 0]
    assert plus_one([9, 9]) == [1, 0, 0]
    assert plus_one([0]) == [1]
    assert plus_one([9]) == [1, 0]
    src = [4, 9]
    assert plus_one(src) == [5, 0] and src == [4, 9]
    assert plus_one([1, 9, 9, 9]) == [2, 0, 0, 0]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
