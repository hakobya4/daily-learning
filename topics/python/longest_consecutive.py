"""
Day 19, Task 3 -- Python: longest consecutive sequence.

THE PROBLEM
------------
Given an unsorted list of integers, return the length of the longest run
of consecutive values (e.g. 3,4,5,6), in O(n) time -- no sorting.
Duplicates count once.

  [100,4,200,1,3,2] -> 4   (1,2,3,4)
  [1,1,1]           -> 1

Raise ValueError if nums is not a list.

HOW TO WORK THROUGH THIS
-------------------------
Put everything in a set. Only start counting from numbers x where x-1 is
NOT in the set, then walk upward.

Run: python3 longest_consecutive.py
"""


def longest_consecutive(nums: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    assert longest_consecutive([1, 1, 1]) == 1
    assert longest_consecutive([-1, 0, 1]) == 3
    assert longest_consecutive([10, 30, 20]) == 1
    try:
        longest_consecutive(None)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
