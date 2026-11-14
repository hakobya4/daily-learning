"""
Day 55, Task 1 -- Python: range module (track half-open intervals with add/remove/query).

THE PROBLEM
------------
Implement RangeModule, which tracks a set of real numbers as a union of HALF-OPEN
intervals [left, right):

  * add_range(left, right)    -- start tracking every number in [left, right).
  * remove_range(left, right) -- stop tracking every number in [left, right).
  * query_range(left, right)  -- True iff EVERY number in [left, right) is tracked.
  * intervals()               -- the tracked set as a sorted list of disjoint,
                                 NON-ADJACENT (left, right) tuples (adjacent pieces such
                                 as [1,3) and [3,5) must be merged into [1,5)).

Rules:
  * left and right are integers with left < right; otherwise raise ValueError (all four
    methods except intervals()).
  * Removing an untracked range is a no-op; adding an already tracked range is a no-op.

Example:
  rm = RangeModule()
  rm.add_range(10, 20); rm.remove_range(14, 16)
  rm.intervals()            -> [(10, 14), (16, 20)]
  rm.query_range(10, 14)    -> True
  rm.query_range(13, 15)    -> False      (14 and 15 are no longer tracked)
  rm.query_range(16, 17)    -> True

Hint: keep two parallel SORTED lists (or one flat list of boundaries) and use
bisect.bisect_left / bisect_right to find the slice of intervals that overlaps or touches
[left, right), then replace that slice in one assignment. Each operation should be
O(log n + k) where k is the number of intervals touched -- no rebuilding everything.

Run: python3 range_module.py
"""


class RangeModule:
    def __init__(self):
        raise NotImplementedError

    def add_range(self, left, right):
        raise NotImplementedError

    def remove_range(self, left, right):
        raise NotImplementedError

    def query_range(self, left, right):
        raise NotImplementedError

    def intervals(self):
        raise NotImplementedError


def _run_tests():
    rm = RangeModule()
    assert rm.intervals() == []
    assert rm.query_range(1, 2) is False
    rm.add_range(10, 20)
    rm.remove_range(14, 16)
    assert rm.intervals() == [(10, 14), (16, 20)]
    assert rm.query_range(10, 14) is True
    assert rm.query_range(13, 15) is False
    assert rm.query_range(16, 17) is True
    assert rm.query_range(19, 20) is True
    assert rm.query_range(19, 21) is False

    # Adjacent ranges merge; overlapping adds merge.
    rm.add_range(14, 16)
    assert rm.intervals() == [(10, 20)]
    rm.add_range(20, 25)
    assert rm.intervals() == [(10, 25)]
    rm.add_range(1, 3)
    rm.add_range(5, 7)
    rm.add_range(2, 6)
    assert rm.intervals() == [(1, 7), (10, 25)]

    # Add spanning several intervals swallows them.
    rm.add_range(30, 31)
    rm.add_range(0, 40)
    assert rm.intervals() == [(0, 40)]

    # Remove punching holes, removing edges, and removing untracked space.
    rm.remove_range(0, 5)
    rm.remove_range(35, 50)
    rm.remove_range(10, 11)
    rm.remove_range(100, 200)
    assert rm.intervals() == [(5, 10), (11, 35)]
    rm.remove_range(5, 35)
    assert rm.intervals() == []

    # Half-open semantics: [1,3) does not cover 3.
    rm.add_range(1, 3)
    assert rm.query_range(1, 3) is True
    assert rm.query_range(2, 4) is False
    rm.remove_range(3, 10)
    assert rm.intervals() == [(1, 3)]

    # Independent instances.
    other = RangeModule()
    other.add_range(50, 60)
    assert rm.intervals() == [(1, 3)] and other.intervals() == [(50, 60)]

    # Invalid ranges.
    for bad in [(5, 5), (6, 2)]:
        for meth in (rm.add_range, rm.remove_range, rm.query_range):
            try:
                meth(*bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"{meth.__name__}{bad} must raise ValueError")

    # Many disjoint intervals stay fast.
    big = RangeModule()
    for i in range(0, 200_000, 2):
        big.add_range(i, i + 1)
    assert len(big.intervals()) == 100_000
    big.add_range(0, 200_000)
    assert big.intervals() == [(0, 200_000)]

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
