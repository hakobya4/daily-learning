"""
Day 18, Task 10 -- CS fundamentals: running median with two heaps.

THE PROBLEM
------------
Implement class RunningMedian with:
  add(x)     -- insert a number, O(log n)
  median()   -- current median in O(1): the middle value for odd counts,
                the mean of the two middle values (a float) for even counts
  __len__    -- number of values added

median() on an empty structure raises ValueError.

  add 5 -> 5; add 15 -> 10.0; add 1 -> 5; add 3 -> 4.0

HOW TO WORK THROUGH THIS
-------------------------
Keep a max-heap `lo` (store negatives with heapq) for the smaller half and
a min-heap `hi` for the larger half; rebalance so len(lo) is len(hi) or
len(hi)+1.

Run: python3 running_median.py
"""


class RunningMedian:
    def __init__(self):
        raise NotImplementedError

    def add(self, x):
        raise NotImplementedError

    def median(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


def _run_tests():
    m = RunningMedian()
    try:
        m.median()
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError on empty median")
    expected = [(5, 5), (15, 10.0), (1, 5), (3, 4.0), (20, 5), (-2, 4.0)]
    for i, (x, med) in enumerate(expected, 1):
        m.add(x)
        assert m.median() == med, (x, m.median(), med)
        assert len(m) == i
    import random
    rnd = random.Random(7)
    m, seen = RunningMedian(), []
    for _ in range(500):
        v = rnd.randint(-100, 100)
        m.add(v)
        seen.append(v)
        s = sorted(seen)
        n = len(s)
        want = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
        assert m.median() == want
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
