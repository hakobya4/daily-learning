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
        self.lo = []  # max-heap (negated values): smaller half
        self.hi = []  # min-heap: larger half

    def add(self, x):
        import heapq
        if self.lo and x > -self.lo[0]:
            heapq.heappush(self.hi, x)
        else:
            heapq.heappush(self.lo, -x)
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        elif len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def median(self):
        if not self.lo:
            raise ValueError("median of empty RunningMedian")
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2

    def __len__(self):
        return len(self.lo) + len(self.hi)


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
