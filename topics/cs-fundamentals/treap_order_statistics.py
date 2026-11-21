"""
Day 62, Task 4 -- CS fundamentals: a treap (randomized BST) with order statistics,
built on split / merge.

THE PROBLEM
------------
A treap is a binary search tree on KEYS that is simultaneously a max-heap on random
PRIORITIES. Random priorities keep the expected depth O(log n) with no rotations
bookkeeping if you build everything from two primitives:

    split(t, key) -> (L, R)   L holds all keys <  key, R holds all keys >= key
    merge(L, R)   -> t        precondition: every key in L < every key in R;
                              the root is whichever of L/R has the higher priority

Each node also stores `size` (number of nodes in its subtree), updated after every
structural change, which gives order statistics in O(log n).

Implement class Treap (a SET of distinct, comparable keys) with:
    insert(key)      -> bool   False if already present (no change)
    remove(key)      -> bool   False if absent
    __contains__(key)
    __len__()
    kth(k)           -> key    0-based k-th smallest; IndexError if k out of range
                               (negative k is out of range too)
    rank(key)        -> int    number of keys strictly less than key (key need not
                               be present)
    range_count(lo, hi) -> int number of keys with lo <= key < hi (0 if lo >= hi)
    __iter__()                 keys in ascending order -- ITERATIVELY (explicit stack),
                               so a degenerate deep tree can't hit the recursion limit
    height()         -> int    0 for empty, 1 for a single node (iterative too)

Use a seeded random.Random passed to the constructor (Treap(seed=...)) for
priorities so runs are reproducible. split/merge may be recursive: the expected
depth is O(log n), and the test checks the height stays small.

Hint: insert = split at key, then merge(merge(L, new_node), R) -- but check
membership first. remove = split at key, split R at the "next" key (or split off the
leftmost node of R), drop the middle, merge back.

Run: python3 treap_order_statistics.py
"""

import random


class _Node:
    __slots__ = ("key", "prio", "left", "right", "size")

    def __init__(self, key, prio):
        self.key = key
        self.prio = prio
        self.left = None
        self.right = None
        self.size = 1


class Treap:
    def __init__(self, seed=None):
        self._rng = random.Random(seed)
        self._root = None

    def insert(self, key):
        raise NotImplementedError

    def remove(self, key):
        raise NotImplementedError

    def __contains__(self, key):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def kth(self, k):
        raise NotImplementedError

    def rank(self, key):
        raise NotImplementedError

    def range_count(self, lo, hi):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def height(self):
        raise NotImplementedError


def _run_tests():
    import bisect
    import math

    t = Treap(seed=1)
    assert len(t) == 0 and list(t) == [] and t.height() == 0
    for k in (0, -1):
        try:
            t.kth(k)
        except IndexError:
            pass
        else:
            raise AssertionError("kth on empty treap must raise IndexError")

    assert t.insert(5) and t.insert(1) and t.insert(9)
    assert not t.insert(5)
    assert list(t) == [1, 5, 9] and len(t) == 3
    assert t.kth(0) == 1 and t.kth(2) == 9
    assert t.rank(5) == 1 and t.rank(6) == 2 and t.rank(0) == 0 and t.rank(100) == 3
    assert t.range_count(1, 9) == 2 and t.range_count(9, 1) == 0 and t.range_count(0, 100) == 3
    assert t.remove(5) and not t.remove(5)
    assert list(t) == [1, 9] and 5 not in t and 9 in t

    words = Treap(seed=2)
    for w in "pear apple fig banana kiwi".split():
        words.insert(w)
    assert list(words) == ["apple", "banana", "fig", "kiwi", "pear"]
    assert words.kth(2) == "fig" and words.rank("cherry") == 2

    # randomized differential test against a sorted list
    rng = random.Random(62)
    t = Treap(seed=3)
    ref = []
    for _ in range(20000):
        op = rng.random()
        x = rng.randrange(3000)
        if op < 0.5:
            pos = bisect.bisect_left(ref, x)
            present = pos < len(ref) and ref[pos] == x
            assert t.insert(x) == (not present)
            if not present:
                ref.insert(pos, x)
        elif op < 0.8:
            pos = bisect.bisect_left(ref, x)
            present = pos < len(ref) and ref[pos] == x
            assert t.remove(x) == present
            if present:
                ref.pop(pos)
        else:
            y = x + rng.randrange(-50, 500)
            assert t.rank(x) == bisect.bisect_left(ref, x)
            assert t.range_count(x, y) == max(0, bisect.bisect_left(ref, y) - bisect.bisect_left(ref, x))
            assert (x in t) == (x in ref)
            if ref:
                k = rng.randrange(len(ref))
                assert t.kth(k) == ref[k]
                try:
                    t.kth(len(ref))
                except IndexError:
                    pass
                else:
                    raise AssertionError("kth(len) must raise IndexError")
    assert list(t) == ref and len(t) == len(ref)

    # sorted insertion would make a plain BST a linked list; a treap stays shallow
    t = Treap(seed=4)
    n = 100_000
    for i in range(n):
        t.insert(i)
    assert len(t) == n and t.kth(n // 2) == n // 2
    assert t.height() <= 4 * math.log2(n), t.height()
    assert sum(1 for _ in t) == n
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
