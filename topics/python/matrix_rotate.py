"""
Day 8, Task 4 -- Python: rotate a matrix 90 degrees clockwise, in place.

THE PROBLEM
------------
Write rotate_90_clockwise(matrix: list[list[int]]) -> list[list[int]]
that rotates an N x N matrix 90 degrees CLOCKWISE, modifying the
matrix's own rows/lists IN PLACE (don't build and return a brand new
list of lists), and also returns that same object for convenience.

"In place" here means: after calling rotate_90_clockwise(m), the
original `m` you passed in should already reflect the rotation --
you're mutating the inner lists, not replacing `matrix` with a new
one.

HOW TO WORK THROUGH THIS
-------------------------
The classic trick is two simple passes, no extra matrix needed:
1. TRANSPOSE the matrix in place (swap matrix[i][j] with matrix[j][i]
   for every i < j -- only need to touch each pair once, not the whole
   grid, and don't touch the diagonal).
2. REVERSE each row in place (row.reverse(), or row[:] = row[::-1]).

Work through why transpose-then-reverse-rows equals a 90-degree
clockwise rotation on paper with a small 3x3 example before coding it
-- seeing which cell ends up where makes the two-step trick click.

Run: python3 matrix_rotate.py
"""


def rotate_90_clockwise(matrix: list[list[int]]) -> list[list[int]]:
    # TODO: transpose in place, then reverse every row in place.
    raise NotImplementedError


def _run_tests() -> None:
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    result = rotate_90_clockwise(m)
    assert result is m, "must mutate and return the SAME object, not a new one"
    assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]], m

    m2 = [[1, 2], [3, 4]]
    rotate_90_clockwise(m2)
    assert m2 == [[3, 1], [4, 2]], m2

    m3 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    rotate_90_clockwise(m3)
    assert m3 == [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]], m3

    m4 = [[5]]
    rotate_90_clockwise(m4)
    assert m4 == [[5]], m4

    print("All matrix_rotate tests passed.")


if __name__ == "__main__":
    _run_tests()
