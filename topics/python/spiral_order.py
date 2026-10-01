"""
Day 10, Task 10 -- Python: spiral order of a matrix.

THE PROBLEM
------------
Write spiral_order(matrix) that returns the elements of a 2D list
(rows x cols, not necessarily square) in clockwise spiral order,
starting at the top-left: right along the top row, down the right
column, left along the bottom row, up the left column, then inward.

  [[1, 2, 3],
   [4, 5, 6],
   [7, 8, 9]]  ->  [1, 2, 3, 6, 9, 8, 7, 4, 5]

An empty matrix (or one with empty rows) returns []. Do not modify the
input.

HOW TO WORK THROUGH THIS
-------------------------
Keep four boundaries (top, bottom, left, right) and shrink them after
walking each side. Watch the single-row / single-column cases so you
don't visit an element twice.

Run: python3 spiral_order.py
"""


def spiral_order(matrix):
    raise NotImplementedError


def _run_tests() -> None:
    assert spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert spiral_order([[1, 2, 3]]) == [1, 2, 3]
    assert spiral_order([[1], [2], [3]]) == [1, 2, 3]
    assert spiral_order([[7]]) == [7]
    assert spiral_order([]) == []
    assert spiral_order([[]]) == []
    m = [[1, 2], [3, 4]]
    assert spiral_order(m) == [1, 2, 4, 3]
    assert m == [[1, 2], [3, 4]]
    print("All spiral_order tests passed.")


if __name__ == "__main__":
    _run_tests()
