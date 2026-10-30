"""
Day 40, Task 8 -- CS fundamentals: k closest points to the origin (heap).

THE PROBLEM
------------
Given a list of (x, y) points and k, return the k points closest to (0, 0)
by Euclidean distance, ordered by increasing distance; ties broken by x then
y ascending. Do not use sqrt (compare squared distances). Use a heap:
heapq.nsmallest / a max-heap of size k, giving O(n log k).

  k_closest([(1, 3), (-2, 2)], 1) -> [(-2, 2)]

HOW TO WORK THROUGH THIS
-------------------------
Key = (x*x + y*y, x, y). A max-heap of size k (store negated keys) keeps the
k smallest while streaming; then sort the survivors by key.

Run: python3 k_closest_points.py
"""
import heapq


def k_closest(points: list, k: int) -> list:
    raise NotImplementedError


def _run_tests():
    assert k_closest([(1, 3), (-2, 2)], 1) == [(-2, 2)]
    assert k_closest([(3, 3), (5, -1), (-2, 4)], 2) == [(3, 3), (-2, 4)]
    assert k_closest([(1, 1), (-1, 1), (1, -1), (-1, -1)], 3) == [(-1, -1), (-1, 1), (1, -1)]
    assert k_closest([], 3) == []
    assert k_closest([(0, 0)], 1) == [(0, 0)]
    assert k_closest([(2, 0), (0, 2), (1, 1)], 3) == [(1, 1), (0, 2), (2, 0)]
    assert k_closest([(5, 5), (1, 0)], 5) == [(1, 0), (5, 5)]
    assert k_closest([(1, 2), (2, 1)], 0) == []
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
