"""
Day 30, Task 9 -- CS fundamentals: partition into two equal-sum subsets.

THE PROBLEM
------------
can_partition(nums) -> True if the list of positive ints can be split into
two subsets with EQUAL sums (every element in exactly one subset).

  [1,5,11,5] -> True   ({11} and {1,5,5})
  [1,2,3,5]  -> False
  []         -> True   (two empty subsets)

HOW TO WORK THROUGH THIS
-------------------------
Odd total -> False. Otherwise it is subset-sum for total//2: a boolean
array reach[0..target], reach[0]=True, iterate items and sums DOWNWARD
(so each item is used at most once). A big-int bitset also works.

Run: python3 partition_equal_subset.py
"""


def can_partition(nums: list) -> bool:
    raise NotImplementedError


def _run_tests():
    assert can_partition([1, 5, 11, 5]) is True
    assert can_partition([1, 2, 3, 5]) is False
    assert can_partition([]) is True
    assert can_partition([2]) is False
    assert can_partition([3, 3]) is True
    assert can_partition([1, 1, 1, 1, 1, 1, 1]) is False
    assert can_partition([100, 100, 100, 100, 99, 101]) is True
    assert can_partition([2, 2, 3, 5]) is False
    assert can_partition(list(range(1, 8))) is True  # sum 28 -> 14
    assert can_partition(list(range(1, 7))) is False  # sum 21 odd
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
