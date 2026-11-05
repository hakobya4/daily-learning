"""
Day 46, Task 1 -- Python: insert an interval into a sorted list.

THE PROBLEM
------------
intervals is a list of non-overlapping [start, end] pairs sorted by start.
insert_interval(intervals, new) returns a NEW sorted list with `new` inserted,
merging every interval it overlaps or touches (end == start counts as touching).
Do not mutate the input. Target O(n), no re-sorting.
Hint: three phases -- copy intervals ending before new, merge the overlapping
ones into new, copy the rest.

Run: python3 insert_interval.py
"""


def insert_interval(intervals, new):
    raise NotImplementedError


def _run_tests():
    assert insert_interval([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert insert_interval([], [5, 7]) == [[5, 7]]
    assert insert_interval([[1, 5]], [2, 3]) == [[1, 5]]
    assert insert_interval([[1, 5]], [6, 8]) == [[1, 5], [6, 8]]
    assert insert_interval([[3, 5]], [1, 2]) == [[1, 2], [3, 5]]
    assert insert_interval([[1, 2], [3, 4]], [2, 3]) == [[1, 4]]
    orig = [[1, 3], [6, 9]]
    insert_interval(orig, [2, 5])
    assert orig == [[1, 3], [6, 9]]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
