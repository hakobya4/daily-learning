"""
Day 34, Task 3 -- Python: search a sorted 2D matrix in O(log(m*n)).

THE PROBLEM
------------
matrix is an m x n grid of integers where each row is sorted ascending and
the first number of each row is greater than the last number of the
previous row. Return True if target is in the matrix, else False, in
O(log(m*n)) time. An empty matrix (or a matrix of empty rows) -> False.

  [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3   -> True
  the same matrix, 13                                     -> False

HOW TO WORK THROUGH THIS
-------------------------
Treat the grid as one sorted list of m*n values: index k maps to
matrix[k // n][k % n]. Then it is an ordinary binary search.

Run: python3 search_matrix.py
"""


def search_matrix(matrix: list, target: int) -> bool:
    if not matrix or not matrix[0]:
        return False
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = matrix[mid // n][mid % n]
        if v == target:
            return True
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def _run_tests():
    m = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    assert search_matrix(m, 3) is True
    assert search_matrix(m, 13) is False
    assert search_matrix(m, 1) is True
    assert search_matrix(m, 60) is True
    assert search_matrix(m, 0) is False
    assert search_matrix(m, 61) is False
    assert search_matrix([[5]], 5) is True
    assert search_matrix([[5]], 4) is False
    assert search_matrix([], 1) is False
    assert search_matrix([[]], 1) is False
    assert search_matrix([[1], [3]], 3) is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
