"""
Day 39, Task 2 -- Python: calendar booking without overlaps.

THE PROBLEM
------------
Implement class MyCalendar with book(start, end) -> bool. Intervals are
half-open [start, end). A booking succeeds (returns True and is stored) only
if it does not overlap any existing booking; otherwise return False and
store nothing. Touching intervals do not overlap: [10,20) and [20,30) are OK.

  c = MyCalendar()
  c.book(10, 20) -> True
  c.book(15, 25) -> False   (overlaps)
  c.book(20, 30) -> True    (touches at 20)

HOW TO WORK THROUGH THIS
-------------------------
Keep a sorted list of starts (and ends). Use bisect to find the neighbours of
the new interval and check only those two: the previous booking must end
<= start, and the next booking must start >= end. O(log n) search per call.

Run: python3 my_calendar.py
"""
import bisect


class MyCalendar:
    def __init__(self):
        self.starts = []
        self.ends = []

    def book(self, start: int, end: int) -> bool:
        i = bisect.bisect_left(self.starts, start)
        if i > 0 and self.ends[i - 1] > start:
            return False
        if i < len(self.starts) and self.starts[i] < end:
            return False
        self.starts.insert(i, start)
        self.ends.insert(i, end)
        return True


def _run_tests():
    c = MyCalendar()
    assert c.book(10, 20) is True
    assert c.book(15, 25) is False
    assert c.book(20, 30) is True
    assert c.book(5, 10) is True
    assert c.book(0, 5) is True
    assert c.book(0, 100) is False
    assert c.book(30, 31) is True
    assert c.book(9, 11) is False
    assert c.book(31, 40) is True
    d = MyCalendar()
    assert d.book(47, 50) is True
    assert d.book(33, 41) is True
    assert d.book(39, 45) is False
    assert d.book(33, 42) is False
    assert d.book(25, 32) is True
    assert d.book(26, 35) is False
    assert d.book(19, 25) is True
    assert d.book(3, 8) is True
    assert d.book(8, 13) is True
    assert d.book(18, 27) is False
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
