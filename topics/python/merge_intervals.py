"""
Day 5, Task 3 -- Python: merge overlapping intervals.

THE PROBLEM
------------
Given a list of intervals, each a [start, end] pair of integers,
possibly unsorted and possibly overlapping, return a new list of
intervals with all overlapping (or touching) intervals merged,
sorted by start. Two intervals [a, b] and [c, d] (with a <= c) should
merge whenever c <= b -- i.e. touching counts as overlapping too, so
[1, 3] and [3, 5] merge into [1, 5].

Example: merge_intervals([[1,3],[2,6],[8,10],[15,18]]) -> [[1,6],[8,10],[15,18]]

HOW TO WORK THROUGH THIS
-------------------------
Sort the intervals by start first. Once sorted, you only ever need to
compare each interval to the LAST interval already placed in your
result list: if the current interval's start is <= that last
interval's end, they overlap -- extend the last interval's end if the
current one reaches further. Otherwise, the current interval doesn't
overlap anything so far -- append it as a new entry.

Run: python3 merge_intervals.py
"""


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda pair: pair[0])
    merged = [list(sorted_intervals[0])]

    for start, end in sorted_intervals[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged


def _run_tests() -> None:
    cases = [
        ([], []),
        ([[1, 3]], [[1, 3]]),
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([[5, 6], [1, 2], [3, 4]], [[1, 2], [3, 4], [5, 6]]),
        ([[1, 10], [2, 3], [4, 5]], [[1, 10]]),
    ]
    for intervals, expected in cases:
        got = merge_intervals(intervals)
        assert got == expected, f"merge_intervals({intervals!r}) -> {got!r}, expected {expected!r}"
    print("All merge_intervals tests passed.")


if __name__ == "__main__":
    _run_tests()
