"""
Day 25, Task 10 -- CS fundamentals: k-th smallest in a row/column-sorted matrix.

THE PROBLEM
------------
matrix is n x n; every row is sorted ascending and every column is sorted
ascending. kth_smallest(matrix, k) returns the k-th smallest element
(1-indexed, duplicates counted). Do NOT just flatten and sort -- use a
min-heap (O(k log n)) or binary search on the value range (O(n log range)).

  matrix = [[ 1,  5,  9],
            [10, 11, 13],
            [12, 13, 15]]
  kth_smallest(matrix, 8) == 13

Raise ValueError if k < 1 or k > n*n.

HOW TO WORK THROUGH THIS
-------------------------
Heap: push (matrix[r][0], r, 0) for each row, pop k times, each time pushing
the next element in that row. Binary search: count elements <= mid by
walking from the bottom-left corner; find the smallest mid with count >= k.

Run: python3 kth_smallest_matrix.py
"""


def kth_smallest(matrix: list, k: int) -> int:
    raise NotImplementedError


def _run_tests():
    m = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
    assert kth_smallest(m, 1) == 1
    assert kth_smallest(m, 8) == 13
    assert kth_smallest(m, 9) == 15
    assert kth_smallest([[-5]], 1) == -5
    assert kth_smallest([[1, 2], [1, 3]], 2) == 1
    assert kth_smallest([[1, 2], [1, 3]], 3) == 2
    big = [[i * 10 + j for j in range(10)] for i in range(10)]
    flat = sorted(x for row in big for x in row)
    for k in (1, 17, 50, 100):
        assert kth_smallest(big, k) == flat[k - 1]
    for bad in (0, 5):
        try:
            kth_smallest([[1, 2], [3, 4]], bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
