"""
Day 29, Task 4 -- Python: set matrix zeroes IN PLACE.

THE PROBLEM
------------
set_zeroes(matrix) modifies the list-of-lists in place: if a cell is 0,
its entire row AND column become 0. Return None. Cells that become 0 must
NOT cause further zeroing (decide from the ORIGINAL matrix only).

  [[1,1,1],[1,0,1],[1,1,1]] -> [[1,0,1],[0,0,0],[1,0,1]]
  [[0,1,2,0],[3,4,5,2],[1,3,1,5]] -> [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

HOW TO WORK THROUGH THIS
-------------------------
Easy: record the zero rows/cols in two sets first (O(m+n) extra space).
Stretch goal: use the first row and first column as the markers for O(1)
extra space (remember separately whether they themselves held a zero).

Run: python3 set_matrix_zeroes.py
"""


def set_zeroes(matrix: list) -> None:
    raise NotImplementedError


def _run_tests():
    m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    assert set_zeroes(m) is None
    assert m == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    m = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    set_zeroes(m)
    assert m == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    m = [[1, 2], [3, 4]]
    set_zeroes(m)
    assert m == [[1, 2], [3, 4]]
    m = [[1, 2, 3]]
    set_zeroes(m)
    assert m == [[1, 2, 3]]
    m = [[1], [0], [3]]
    set_zeroes(m)
    assert m == [[0], [0], [0]]
    m = [[0]]
    set_zeroes(m)
    assert m == [[0]]
    m = []
    set_zeroes(m)
    assert m == []
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
