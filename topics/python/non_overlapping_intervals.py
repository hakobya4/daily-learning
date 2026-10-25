"""
Day 35, Task 2 -- Python: non-overlapping intervals (greedy).

THE PROBLEM
------------
Given a list of [start, end] intervals, return the MINIMUM number of
intervals to remove so that the rest do not overlap. Intervals that only
touch at an endpoint ([1,2] and [2,3]) do NOT overlap.

  [[1,2],[2,3],[3,4],[1,3]]  -> 1   (remove [1,3])
  [[1,2],[1,2],[1,2]]        -> 2
  [[1,2],[2,3]]              -> 0

HOW TO WORK THROUGH THIS
-------------------------
Sort by END. Keep the interval that ends earliest; any later interval whose
start is < the last kept end overlaps and is removed (count it), otherwise
keep it and update the last end.

Run: python3 non_overlapping_intervals.py
"""


def erase_overlap_intervals(intervals: list) -> int:
    if not intervals:
        return 0
    removed = 0
    last_end = None
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if last_end is None or start >= last_end:
            last_end = end
        else:
            removed += 1
    return removed


def _run_tests():
    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0
    assert erase_overlap_intervals([]) == 0
    assert erase_overlap_intervals([[0, 10], [1, 2], [3, 4], [5, 6]]) == 1
    assert erase_overlap_intervals([[1, 100], [11, 22], [1, 11], [2, 12]]) == 2
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
