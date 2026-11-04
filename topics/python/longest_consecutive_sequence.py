"""
Day 45, Task 1 -- Python: longest consecutive sequence.

THE PROBLEM
------------
longest_consecutive(nums) returns the length of the longest run of
consecutive integers (e.g. 4,5,6,7) that can be formed from the values in
nums, in any order, ignoring duplicates. Must run in O(n) expected time.
Empty input -> 0.
Hint: put the numbers in a set; only start counting at numbers whose x-1 is
not in the set.

Run: python3 longest_consecutive_sequence.py
"""


def longest_consecutive(nums):
    raise NotImplementedError


def _run_tests():
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    assert longest_consecutive([5]) == 1
    assert longest_consecutive([1, 1, 1]) == 1
    assert longest_consecutive([-2, -1, 0, 10]) == 3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
