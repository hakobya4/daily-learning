"""
Day 26, Task 10 -- CS fundamentals: 2D range sum with prefix sums.

THE PROBLEM
------------
Implement class NumMatrix(matrix) with sum_region(r1, c1, r2, c2) that
returns the sum of all cells in the inclusive rectangle with top-left
(r1, c1) and bottom-right (r2, c2). Precompute in the constructor so each
query is O(1).

HOW TO WORK THROUGH THIS
-------------------------
Build P of size (rows+1) x (cols+1) where P[i][j] is the sum of the
rectangle (0,0)..(i-1,j-1). Then
  sum = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]

Run: python3 num_matrix_2d.py
"""


class NumMatrix:
    def __init__(self, matrix: list):
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        self.P = [[0] * (cols + 1) for _ in range(rows + 1)]
        for i in range(rows):
            for j in range(cols):
                self.P[i + 1][j + 1] = (matrix[i][j] + self.P[i][j + 1]
                                        + self.P[i + 1][j] - self.P[i][j])

    def sum_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        P = self.P
        return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]


def _run_tests():
    m = NumMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert m.sum_region(0, 0, 2, 2) == 45
    assert m.sum_region(1, 1, 2, 2) == 28
    assert m.sum_region(0, 1, 1, 1) == 7
    assert m.sum_region(2, 0, 2, 0) == 7
    assert m.sum_region(0, 0, 0, 0) == 1
    n = NumMatrix([[-1, 4], [3, -2]])
    assert n.sum_region(0, 0, 1, 1) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
