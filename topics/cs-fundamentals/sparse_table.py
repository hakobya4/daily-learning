"""
Day 29, Task 9 -- CS fundamentals: sparse table for range-minimum queries.

THE PROBLEM
------------
Implement class SparseTable(values):
  - build in O(n log n): table[k][i] = min of values[i : i + 2**k]
  - query(l, r) -> minimum of values[l..r] INCLUSIVE, in O(1), by
    overlapping two power-of-two blocks:
        k = floor(log2(r - l + 1));  min(table[k][l], table[k][r - 2**k + 1])
  - raise ValueError if l > r or an index is out of range.

  SparseTable([5, 2, 4, 7, 1, 3]).query(0, 3) -> 2
  SparseTable([5, 2, 4, 7, 1, 3]).query(3, 5) -> 1
  SparseTable([5]).query(0, 0)               -> 5

HOW TO WORK THROUGH THIS
-------------------------
Level k+1 is built from level k:
    table[k+1][i] = min(table[k][i], table[k][i + 2**k]).
Use int.bit_length() - 1 for floor(log2). Works because min is idempotent
(overlap is harmless) -- think about why this FAILS for sum.

Run: python3 sparse_table.py
"""


class SparseTable:
    def __init__(self, values):
        self.n = len(values)
        self.table = [list(values)]
        k = 0
        while (1 << (k + 1)) <= self.n:
            prev = self.table[k]
            half = 1 << k
            self.table.append([min(prev[i], prev[i + half])
                               for i in range(self.n - (1 << (k + 1)) + 1)])
            k += 1

    def query(self, l, r):
        if l > r or l < 0 or r >= self.n:
            raise ValueError("invalid range")
        k = (r - l + 1).bit_length() - 1
        return min(self.table[k][l], self.table[k][r - (1 << k) + 1])


def _run_tests():
    import random
    t = SparseTable([5, 2, 4, 7, 1, 3])
    assert t.query(0, 3) == 2
    assert t.query(3, 5) == 1
    assert t.query(2, 2) == 4
    assert t.query(0, 5) == 1
    assert SparseTable([5]).query(0, 0) == 5
    for bad in [(3, 2), (-1, 2), (0, 6)]:
        try:
            t.query(*bad)
            assert False, f"expected ValueError for {bad}"
        except ValueError:
            pass
    random.seed(7)
    vals = [random.randint(-50, 50) for _ in range(200)]
    t = SparseTable(vals)
    for _ in range(500):
        l = random.randrange(200)
        r = random.randrange(l, 200)
        assert t.query(l, r) == min(vals[l:r + 1])
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
