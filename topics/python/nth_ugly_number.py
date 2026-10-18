"""
Day 28, Task 3 -- Python: nth ugly number.

THE PROBLEM
------------
An ugly number is a positive integer whose only prime factors are 2, 3
and 5. By convention 1 is ugly. nth_ugly(n) returns the n-th ugly number
(1-based).

  sequence: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, ...
  nth_ugly(1)  -> 1
  nth_ugly(10) -> 12
  nth_ugly(11) -> 15

Raise ValueError if n < 1.

HOW TO WORK THROUGH THIS
-------------------------
Don't test every integer. Build the list with three pointers (one each
for the 2x, 3x, 5x candidates) and take the minimum each step: O(n).

Run: python3 nth_ugly_number.py
"""


def nth_ugly(n: int) -> int:
    raise NotImplementedError


def _run_tests():
    assert [nth_ugly(i) for i in range(1, 13)] == [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16]
    assert nth_ugly(15) == 24
    assert nth_ugly(100) == 1536
    assert nth_ugly(1690) == 2123366400
    for bad in (0, -3):
        try:
            nth_ugly(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for n=%d" % bad)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
