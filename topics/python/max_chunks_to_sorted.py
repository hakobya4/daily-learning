"""
Day 39, Task 3 -- Python: max chunks to make sorted.

THE PROBLEM
------------
arr is a permutation of 0..n-1. Split it into the maximum number of
contiguous chunks such that sorting each chunk individually and concatenating
the chunks yields the fully sorted array. Return that maximum count.

  [4, 3, 2, 1, 0]  -> 1
  [1, 0, 2, 3, 4]  -> 4   ([1,0] [2] [3] [4])
  [0, 1, 2]        -> 3
  []               -> 0

HOW TO WORK THROUGH THIS
-------------------------
Scan left to right tracking the running maximum. If the running max equals
the current index i, then everything seen so far is exactly {0..i}, so a
chunk can end here. Count those positions. O(n).

Run: python3 max_chunks_to_sorted.py
"""


def max_chunks_to_sorted(arr: list) -> int:
    count = 0
    running_max = -1
    for i, v in enumerate(arr):
        running_max = max(running_max, v)
        if running_max == i:
            count += 1
    return count


def _run_tests():
    assert max_chunks_to_sorted([4, 3, 2, 1, 0]) == 1
    assert max_chunks_to_sorted([1, 0, 2, 3, 4]) == 4
    assert max_chunks_to_sorted([0, 1, 2]) == 3
    assert max_chunks_to_sorted([]) == 0
    assert max_chunks_to_sorted([0]) == 1
    assert max_chunks_to_sorted([1, 2, 0, 3]) == 2
    assert max_chunks_to_sorted([2, 0, 1, 4, 3, 5]) == 3
    assert max_chunks_to_sorted(list(range(100))) == 100
    assert max_chunks_to_sorted(list(range(99, -1, -1))) == 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
