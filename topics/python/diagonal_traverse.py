"""
Day 25, Task 4 -- Python: zig-zag diagonal traversal of a matrix.

THE PROBLEM
------------
diagonal_traverse(matrix) returns all elements of an m x n matrix in
diagonal zig-zag order: start at the top-left going up-right, bounce off
the border, then go down-left, and so on.

  [[1, 2, 3],
   [4, 5, 6],
   [7, 8, 9]]   ->  [1, 2, 4, 7, 5, 3, 6, 8, 9]

An empty matrix (or one with empty rows) returns [].

HOW TO WORK THROUGH THIS
-------------------------
Elements on the same diagonal share r + c. Collect each diagonal, and
reverse every other one. Or simulate with a direction and fix up when you
leave the grid.

Run: python3 diagonal_traverse.py
"""


def diagonal_traverse(matrix: list) -> list:
    if not matrix or not matrix[0]:
        return []
    m, n = len(matrix), len(matrix[0])
    out = []
    for d in range(m + n - 1):
        diag = [matrix[r][d - r] for r in range(max(0, d - n + 1), min(m - 1, d) + 1)]
        # diag runs top-to-bottom (down-left); even d goes up-right
        out.extend(reversed(diag) if d % 2 == 0 else diag)
    return out


def _run_tests():
    assert diagonal_traverse([]) == []
    assert diagonal_traverse([[]]) == []
    assert diagonal_traverse([[5]]) == [5]
    assert diagonal_traverse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 4, 7, 5, 3, 6, 8, 9]
    assert diagonal_traverse([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert diagonal_traverse([[1, 2, 3, 4]]) == [1, 2, 3, 4]
    assert diagonal_traverse([[1], [2], [3]]) == [1, 2, 3]
    assert diagonal_traverse([[1, 2, 3], [4, 5, 6]]) == [1, 2, 4, 5, 3, 6]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
