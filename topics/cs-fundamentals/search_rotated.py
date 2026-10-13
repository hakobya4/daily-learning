"""
Day 23, Task 9 -- CS fundamentals: search in a rotated sorted array.

THE PROBLEM
------------
nums was sorted ascending (all values distinct) and then rotated at an
unknown pivot, e.g. [0,1,2,4,5,6,7] -> [4,5,6,7,0,1,2]. Return the index
of target, or -1 if absent, in O(log n) time (no linear scan, no
list.index).

  search_rotated([4,5,6,7,0,1,2], 0) == 4
  search_rotated([4,5,6,7,0,1,2], 3) == -1
  search_rotated([1], 1) == 0

HOW TO WORK THROUGH THIS
-------------------------
Binary search: at each step one half [lo..mid] or [mid..hi] is properly
sorted. Decide which, check whether target lies inside it, and discard
the other half.

Run: python3 search_rotated.py
"""


def search_rotated(nums: list, target: int) -> int:
    raise NotImplementedError


def _run_tests():
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search_rotated([1], 1) == 0
    assert search_rotated([1], 0) == -1
    assert search_rotated([], 5) == -1
    assert search_rotated([3, 1], 1) == 1
    base = list(range(0, 200, 2))
    for r in range(len(base)):
        arr = base[r:] + base[:r]
        for i, v in enumerate(arr):
            assert search_rotated(arr, v) == i
        assert search_rotated(arr, 1) == -1
        assert search_rotated(arr, 500) == -1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
