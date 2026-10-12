"""
Day 22, Task 9 -- CS fundamentals: quickselect.

THE PROBLEM
------------
Implement quickselect(items, k) returning the k-th SMALLEST element
(k is 0-indexed, so k=0 is the minimum) in expected O(n) time, WITHOUT
fully sorting and WITHOUT modifying the caller's list.

  quickselect([7, 2, 9, 4, 1], 0) == 1
  quickselect([7, 2, 9, 4, 1], 2) == 4
  quickselect([5, 5, 5, 5], 3)    == 5

Must handle duplicates. Raise IndexError if k is out of range.

HOW TO WORK THROUGH THIS
-------------------------
Pick a random pivot, partition into less / equal / greater, then recurse
(or loop) into only the side that contains index k.

Run: python3 quickselect.py
"""


def quickselect(items: list, k: int):
    raise NotImplementedError


def _run_tests():
    import random
    assert quickselect([7, 2, 9, 4, 1], 0) == 1
    assert quickselect([7, 2, 9, 4, 1], 2) == 4
    assert quickselect([7, 2, 9, 4, 1], 4) == 9
    assert quickselect([5, 5, 5, 5], 3) == 5
    assert quickselect([42], 0) == 42
    data = [3, 1, 2]
    quickselect(data, 1)
    assert data == [3, 1, 2], "input must not be modified"
    rng = random.Random(7)
    for _ in range(200):
        xs = [rng.randint(-20, 20) for _ in range(rng.randint(1, 40))]
        k = rng.randrange(len(xs))
        assert quickselect(xs, k) == sorted(xs)[k]
    for bad_items, bad_k in (([], 0), ([1, 2], 2), ([1, 2], -1)):
        try:
            quickselect(bad_items, bad_k)
        except IndexError:
            pass
        else:
            raise AssertionError("expected IndexError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
