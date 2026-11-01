"""
Day 41, Task 2 -- Python: rotate a square matrix in place.

THE PROBLEM
------------
rotate(m) rotates an n x n matrix (list of lists) 90 degrees CLOCKWISE
IN PLACE (mutate m, return None, no new n x n allocation).

  [[1,2,3],        [[7,4,1],
   [4,5,6],   ->    [8,5,2],
   [7,8,9]]         [9,6,3]]

HINT: transpose, then reverse each row.

Run: python3 rotate_matrix.py
"""


def rotate(m: list) -> None:
    raise NotImplementedError


def _run_tests():
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert rotate(a) is None
    assert a == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    b = [[1, 2], [3, 4]]
    rotate(b)
    assert b == [[3, 1], [4, 2]]
    c = [[5]]
    rotate(c)
    assert c == [[5]]
    d = [[i * 4 + j for j in range(4)] for i in range(4)]
    for _ in range(4):
        rotate(d)
    assert d == [[i * 4 + j for j in range(4)] for i in range(4)]
    d2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    rotate(d2)
    assert d2 == [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
