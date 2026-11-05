"""
Day 46, Task 2 -- Python: missing ranges.

THE PROBLEM
------------
nums is a sorted list of distinct integers, all within [lo, hi].
missing_ranges(nums, lo, hi) returns the list of strings describing every
number in [lo, hi] absent from nums: a single gap number as "5", a longer gap
as "7->10". Return [] if nothing is missing.
Hint: walk with a `prev` starting at lo-1, and compare each x (and finally hi+1).

Run: python3 find_missing_ranges.py
"""


def missing_ranges(nums, lo, hi):
    raise NotImplementedError


def _run_tests():
    assert missing_ranges([0, 1, 3, 50, 75], 0, 99) == ["2", "4->49", "51->74", "76->99"]
    assert missing_ranges([], 1, 1) == ["1"]
    assert missing_ranges([], 1, 4) == ["1->4"]
    assert missing_ranges([1, 2, 3], 1, 3) == []
    assert missing_ranges([-1], -1, -1) == []
    assert missing_ranges([2], 1, 3) == ["1", "3"]
    assert missing_ranges([5], 1, 5) == ["1->4"]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
