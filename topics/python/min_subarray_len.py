"""
Day 27, Task 2 -- Python: minimum size subarray sum.

THE PROBLEM
------------
min_subarray_len(target, nums) returns the length of the shortest
contiguous subarray of POSITIVE integers whose sum is >= target, or 0 if
no such subarray exists.

  min_subarray_len(7, [2, 3, 1, 2, 4, 3]) -> 2   ([4, 3])
  min_subarray_len(100, [1, 2, 3])        -> 0

HOW TO WORK THROUGH THIS
-------------------------
Sliding window: grow the right end, and while the window sum is >= target
shrink from the left, recording the shortest length. O(n).

Run: python3 min_subarray_len.py
"""


def min_subarray_len(target: int, nums: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert min_subarray_len(4, [1, 4, 4]) == 1
    assert min_subarray_len(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
    assert min_subarray_len(100, [1, 2, 3]) == 0
    assert min_subarray_len(15, [1, 2, 3, 4, 5]) == 5
    assert min_subarray_len(5, []) == 0
    assert min_subarray_len(3, [1, 1, 1]) == 3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
