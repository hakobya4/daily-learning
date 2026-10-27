"""
Day 37, Task 4 -- Python: find all duplicates in an array in O(n) time, O(1) extra space.

THE PROBLEM
------------
nums has length n and every value is in 1..n; each value appears once or
twice. Return a sorted list of the values that appear twice. Aim for O(n)
time and no extra data structure (the output list does not count).
You may modify nums.

  [4,3,2,7,8,2,3,1] -> [2, 3]
  [1,1,2]           -> [1]
  [1]               -> []

HOW TO WORK THROUGH THIS
-------------------------
Use the sign of nums[abs(x) - 1] as a "seen" flag: for each x, if that
slot is already negative then abs(x) is a duplicate, otherwise negate it.
Sort the result at the end.

Run: python3 find_all_duplicates.py
"""


def find_duplicates(nums: list) -> list:
    raise NotImplementedError


def _run_tests():
    assert find_duplicates([4, 3, 2, 7, 8, 2, 3, 1]) == [2, 3]
    assert find_duplicates([1, 1, 2]) == [1]
    assert find_duplicates([1]) == []
    assert find_duplicates([1, 2, 3]) == []
    assert find_duplicates([2, 2]) == [2]
    assert find_duplicates([3, 3, 1, 1, 2]) == [1, 3]
    assert find_duplicates([]) == []
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
