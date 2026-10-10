"""
Day 20, Task 10 -- CS fundamentals: Fenwick tree (binary indexed tree).

THE PROBLEM
------------
Support point updates and prefix sums in O(log n) on an array of n
integers (0-indexed from the caller's point of view).

  FenwickTree(n)                 n zeros
  FenwickTree.from_list(values)  build from a list
  add(i, delta)                  values[i] += delta
  prefix_sum(i)                  sum of values[0..i] inclusive (i=-1 -> 0)
  range_sum(l, r)                sum of values[l..r] inclusive

Raise IndexError for indexes outside 0..n-1 (prefix_sum accepts -1 too),
ValueError if n < 0 or if l > r.

HOW TO WORK THROUGH THIS
-------------------------
Internally 1-indexed; i += i & -i walks up for updates, i -= i & -i walks
down for queries.

Run: python3 fenwick_tree.py
"""

import random


class FenwickTree:
    def __init__(self, n: int):
        raise NotImplementedError

    @classmethod
    def from_list(cls, values: list) -> "FenwickTree":
        raise NotImplementedError

    def add(self, i: int, delta: int) -> None:
        raise NotImplementedError

    def prefix_sum(self, i: int) -> int:
        raise NotImplementedError

    def range_sum(self, l: int, r: int) -> int:
        raise NotImplementedError


def _run_tests():
    ft = FenwickTree.from_list([3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3])
    assert ft.prefix_sum(-1) == 0
    assert ft.prefix_sum(0) == 3
    assert ft.prefix_sum(4) == 15
    assert ft.range_sum(2, 5) == 14
    ft.add(3, 10)
    assert ft.range_sum(2, 5) == 24
    assert ft.range_sum(3, 3) == 16
    z = FenwickTree(0)
    assert z.prefix_sum(-1) == 0
    for bad in (lambda: ft.add(11, 1), lambda: ft.prefix_sum(11),
                lambda: ft.range_sum(-1, 2)):
        try:
            bad()
        except IndexError:
            pass
        else:
            raise AssertionError("expected IndexError")
    for bad in (lambda: FenwickTree(-1), lambda: ft.range_sum(5, 2)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    rng = random.Random(7)
    vals = [rng.randint(-50, 50) for _ in range(200)]
    ft = FenwickTree.from_list(vals)
    for _ in range(500):
        i = rng.randrange(200)
        d = rng.randint(-20, 20)
        vals[i] += d
        ft.add(i, d)
        l = rng.randrange(200)
        r = rng.randrange(l, 200)
        assert ft.range_sum(l, r) == sum(vals[l:r + 1])
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
