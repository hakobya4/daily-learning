"""
Day 15, Task 3 -- Python: meeting rooms.

THE PROBLEM
------------
Meetings are (start, end) pairs with start < end; a meeting ending at
time t does NOT conflict with one starting at t.

    can_attend_all([(0, 30), (35, 40)])        -> True
    can_attend_all([(0, 30), (15, 20)])        -> False
    min_rooms([(0, 30), (5, 10), (15, 20)])    -> 2
    min_rooms([(1, 2), (2, 3)])                -> 1
    min_rooms([])                              -> 0

Also implement busiest_time(meetings) -> the earliest start time at
which the maximum number of meetings overlap (None for []).

HOW TO WORK THROUGH THIS
-------------------------
Sort starts and ends separately and sweep with two pointers, or use a
min-heap of end times. Process an end before a start at the same time.

Run: python3 meeting_rooms.py
"""


def can_attend_all(meetings: list[tuple[int, int]]) -> bool:
    ordered = sorted(meetings)
    return all(ordered[i][1] <= ordered[i + 1][0] for i in range(len(ordered) - 1))


def _sweep(meetings):
    # events: (time, delta); ends (-1) sort before starts (+1) at the same time
    events = sorted([(s, 1) for s, _ in meetings] + [(e, -1) for _, e in meetings])
    cur = best = 0
    best_time = None
    for t, d in events:
        cur += d
        if cur > best:
            best, best_time = cur, t
    return best, best_time


def min_rooms(meetings: list[tuple[int, int]]) -> int:
    return _sweep(meetings)[0]


def busiest_time(meetings: list[tuple[int, int]]):
    return _sweep(meetings)[1]


def _run_tests() -> None:
    assert can_attend_all([(0, 30), (35, 40)]) is True
    assert can_attend_all([(0, 30), (15, 20)]) is False
    assert can_attend_all([(1, 2), (2, 3)]) is True
    assert can_attend_all([]) is True
    assert min_rooms([(0, 30), (5, 10), (15, 20)]) == 2
    assert min_rooms([(1, 2), (2, 3)]) == 1
    assert min_rooms([]) == 0
    assert min_rooms([(1, 5), (2, 6), (3, 7), (4, 8)]) == 4
    m = [(9, 12), (10, 11), (10, 13), (14, 15)]
    assert min_rooms(m) == 3
    assert m == [(9, 12), (10, 11), (10, 13), (14, 15)]  # input untouched
    assert busiest_time(m) == 10
    assert busiest_time([]) is None
    assert busiest_time([(1, 2), (5, 6)]) == 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
