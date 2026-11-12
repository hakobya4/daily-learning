"""
Day 53, Task 10 -- Python: snapshot array (per-index version history + bisect).

THE PROBLEM
------------
Implement SnapshotArray(length): an array of `length` integers, all initially 0.
  set(index, val)      -- set the element at index to val.
  snap()               -- take a snapshot and return its id: 0 for the first call, then 1, 2, ...
  get(index, snap_id)  -- the value at index at the moment snapshot snap_id was taken.
Copying the whole array on every snap() is too slow/large for big arrays with few changes.
Hint: per index keep a list of (snap_id, value) pairs, overwriting the last pair when it has
the current snap id; get() uses bisect to find the last pair with id <= snap_id.
Raise IndexError for an index outside 0..length-1, and ValueError in get() for a snap_id
that has not been returned by snap() yet.

Run: python3 snapshot_array.py
"""


class SnapshotArray:
    def __init__(self, length):
        raise NotImplementedError

    def set(self, index, val):
        raise NotImplementedError

    def snap(self):
        raise NotImplementedError

    def get(self, index, snap_id):
        raise NotImplementedError


def _run_tests():
    a = SnapshotArray(3)
    a.set(0, 5)
    assert a.snap() == 0
    a.set(0, 6)
    assert a.get(0, 0) == 5
    assert a.get(1, 0) == 0

    b = SnapshotArray(4)
    assert b.snap() == 0
    assert b.snap() == 1
    b.set(2, 7)
    b.set(2, 8)          # overwrite before the next snap
    assert b.snap() == 2
    b.set(2, 9)
    assert b.snap() == 3
    assert b.get(2, 0) == 0
    assert b.get(2, 1) == 0
    assert b.get(2, 2) == 8
    assert b.get(2, 3) == 9
    assert b.get(3, 3) == 0

    c = SnapshotArray(1)
    for v in range(5):
        c.set(0, v * 10)
        c.snap()
    assert [c.get(0, s) for s in range(5)] == [0, 10, 20, 30, 40]

    for bad in (lambda: c.set(1, 1), lambda: c.get(-1, 0), lambda: c.get(5, 0)):
        try:
            bad()
        except IndexError:
            pass
        else:
            raise AssertionError("expected IndexError")
    try:
        c.get(0, 5)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a snap_id not taken yet")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
