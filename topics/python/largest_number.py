"""
Day 23, Task 2 -- Python: largest number from concatenation.

THE PROBLEM
------------
Given a list of non-negative integers, arrange them so that their
concatenation is the largest possible number. Return it as a STRING.

  largest_number([10, 2])            == "210"
  largest_number([3, 30, 34, 5, 9])  == "9534330"
  largest_number([0, 0])             == "0"      (no leading zeros)
  largest_number([])                 == ""

HOW TO WORK THROUGH THIS
-------------------------
Compare two numbers a, b as strings by which of a+b or b+a is larger.
Use functools.cmp_to_key to sort with that comparison, then join. Watch
the all-zeros case.

Run: python3 largest_number.py
"""


def largest_number(nums: list) -> str:
    raise NotImplementedError


def _run_tests():
    assert largest_number([10, 2]) == "210"
    assert largest_number([3, 30, 34, 5, 9]) == "9534330"
    assert largest_number([0, 0]) == "0"
    assert largest_number([]) == ""
    assert largest_number([1]) == "1"
    assert largest_number([121, 12]) == "12121"
    assert largest_number([824, 8247]) == "8248247"
    assert largest_number([0, 0, 1]) == "100"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
