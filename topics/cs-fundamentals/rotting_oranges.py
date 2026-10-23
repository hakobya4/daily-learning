"""
Day 33, Task 9 -- CS fundamentals: rotting oranges (multi-source BFS).

THE PROBLEM
------------
grid is a list of lists with cells:
  0 = empty, 1 = fresh orange, 2 = rotten orange.
Every minute, each fresh orange that is 4-directionally adjacent to a
rotten one becomes rotten. Return the minimum number of minutes until no
fresh orange remains, or -1 if that is impossible.

  [[2,1,1],[1,1,0],[0,1,1]] -> 4
  [[2,1,1],[0,1,1],[1,0,1]] -> -1   (bottom-left orange is cut off)
  [[0,2]]                   -> 0    (nothing fresh)

HOW TO WORK THROUGH THIS
-------------------------
Start a BFS with ALL rotten oranges in the queue at once (multi-source),
process the queue level by level (one level = one minute), and count the
fresh oranges so you can tell whether any are left at the end. Do not
mutate the caller's grid.

Run: python3 rotting_oranges.py
"""


def oranges_rotting(grid: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert oranges_rotting([[0, 2]]) == 0
    assert oranges_rotting([[0]]) == 0
    assert oranges_rotting([[1]]) == -1
    assert oranges_rotting([[2, 2], [2, 2]]) == 0
    assert oranges_rotting([[2, 1], [1, 1]]) == 2
    assert oranges_rotting([[2, 1, 1, 1, 1, 2]]) == 2
    g = [[2, 1], [1, 1]]
    oranges_rotting(g)
    assert g == [[2, 1], [1, 1]], "grid must not be mutated"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
