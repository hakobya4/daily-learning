"""
Day 15, Task 9 -- CS fundamentals: kth largest element (heap / quickselect).

THE PROBLEM
------------
kth_largest(nums, k) -> the k-th largest value (1-based, duplicates
count separately), WITHOUT fully sorting the list in your solution.
Raise ValueError if k < 1 or k > len(nums).

    kth_largest([3, 2, 1, 5, 6, 4], 2)          -> 5
    kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) -> 4

Also implement the streaming version:

    class KthLargest:
        def __init__(self, k, nums): ...
        def add(self, val) -> int   # returns current k-th largest

    kl = KthLargest(3, [4, 5, 8, 2]); kl.add(3) -> 4; kl.add(5) -> 5

Use a min-heap of size k (heapq is allowed). Do not mutate `nums`.

HOW TO WORK THROUGH THIS
-------------------------
Keep the k largest seen so far in a min-heap; the root is the answer.
For add(): push, then pop if the heap grew beyond k.

Run: python3 kth_largest.py
"""


def kth_largest(nums: list[int], k: int) -> int:
    raise NotImplementedError


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        raise NotImplementedError

    def add(self, val: int) -> int:
        raise NotImplementedError


def _run_tests() -> None:
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert kth_largest([7], 1) == 7
    assert kth_largest([1, 1, 1], 3) == 1
    n = [5, 1, 4]
    kth_largest(n, 1)
    assert n == [5, 1, 4]
    for bad in (0, 4, -1):
        try:
            kth_largest([1, 2, 3], bad)
            assert False, "expected ValueError"
        except ValueError:
            pass
    kl = KthLargest(3, [4, 5, 8, 2])
    assert kl.add(3) == 4
    assert kl.add(5) == 5
    assert kl.add(10) == 5
    assert kl.add(9) == 8
    assert kl.add(4) == 8
    kl2 = KthLargest(1, [])
    assert kl2.add(-3) == -3
    assert kl2.add(-5) == -3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
