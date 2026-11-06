"""
Day 47, Task 9 -- CS fundamentals: longest increasing path in a matrix (DFS + memoization).

THE PROBLEM
------------
Given an m x n integer matrix, return the length of the longest strictly
increasing path. From each cell you may move up, down, left or right (no
diagonals, no wrapping). Empty matrix -> 0.
Target O(m*n): memoize the best path starting at each cell. Mind recursion
depth on big inputs (an iterative topological order also works).

Run: python3 longest_increasing_path.py
"""


def longest_increasing_path(matrix):
    raise NotImplementedError


def _run_tests():
    assert longest_increasing_path([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4
    assert longest_increasing_path([[3, 4, 5], [3, 2, 6], [2, 2, 1]]) == 4
    assert longest_increasing_path([[1]]) == 1
    assert longest_increasing_path([]) == 0
    assert longest_increasing_path([[1, 2, 3, 4]]) == 4
    assert longest_increasing_path([[5, 5], [5, 5]]) == 1
    n = 30
    snake = [[r * n + c for c in range(n)] for r in range(n)]
    assert longest_increasing_path(snake) == 2 * n - 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
