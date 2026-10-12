"""
Day 21, Task 9 -- CS fundamentals: segment tree (range minimum).

THE PROBLEM
------------
Implement class SegmentTree(values) supporting:

  update(i, v)  -- set values[i] = v        in O(log n)
  query(l, r)   -- minimum of values[l:r]   in O(log n), half-open range

Raise IndexError for an i outside the array, and ValueError for an empty
or out-of-bounds query range (l >= r, l < 0, r > n).

HOW TO WORK THROUGH THIS
-------------------------
Iterative bottom-up layout: store leaves at tree[n + i], internal node j
is min(tree[2j], tree[2j+1]). Query walks l and r upward.

Run: python3 segment_tree.py
"""


class SegmentTree:
    def __init__(self, values):
        self.n = len(values)
        self.tree = [float("inf")] * self.n + list(values)
        for j in range(self.n - 1, 0, -1):
            self.tree[j] = min(self.tree[2 * j], self.tree[2 * j + 1])

    def update(self, i: int, v) -> None:
        if not 0 <= i < self.n:
            raise IndexError(i)
        j = i + self.n
        self.tree[j] = v
        j //= 2
        while j >= 1:
            self.tree[j] = min(self.tree[2 * j], self.tree[2 * j + 1])
            j //= 2

    def query(self, l: int, r: int):
        if l < 0 or r > self.n or l >= r:
            raise ValueError((l, r))
        res = float("inf")
        l += self.n
        r += self.n
        while l < r:
            if l & 1:
                res = min(res, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = min(res, self.tree[r])
            l //= 2
            r //= 2
        return res


def _run_tests():
    import random

    st = SegmentTree([5, 2, 8, 1, 9, 3])
    assert st.query(0, 6) == 1
    assert st.query(0, 3) == 2
    assert st.query(4, 6) == 3
    assert st.query(2, 3) == 8
    st.update(3, 10)
    assert st.query(0, 6) == 2
    assert st.query(2, 4) == 8
    for bad in [(3, 3), (-1, 2), (0, 7), (4, 2)]:
        try:
            st.query(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")
    try:
        st.update(6, 0)
    except IndexError:
        pass
    else:
        raise AssertionError("expected IndexError")

    rnd = random.Random(7)
    for n in (1, 2, 7, 33):
        arr = [rnd.randint(-50, 50) for _ in range(n)]
        t = SegmentTree(arr)
        for _ in range(300):
            if rnd.random() < 0.4:
                i, v = rnd.randrange(n), rnd.randint(-50, 50)
                arr[i] = v
                t.update(i, v)
            else:
                l = rnd.randrange(n)
                r = rnd.randint(l + 1, n)
                assert t.query(l, r) == min(arr[l:r])
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
