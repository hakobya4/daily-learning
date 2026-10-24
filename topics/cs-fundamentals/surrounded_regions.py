"""
Day 34, Task 10 -- CS fundamentals: surrounded regions (border flood fill).

THE PROBLEM
------------
board is a grid of "X" and "O". Capture every region of "O" cells that is
completely surrounded by "X" (4-directional adjacency) by flipping all its
cells to "X". An "O" region that touches the border (or is connected to a
border "O") is NOT captured. Modify board in place and also return it.

  XXXX        XXXX
  XOOX   ->   XXXX
  XXOX        XXXX
  XOXX        XOXX      (bottom "O" is on the border, so it stays)

HOW TO WORK THROUGH THIS
-------------------------
Start from every border "O" and flood-fill (BFS/DFS) marking reachable
"O" cells as safe (e.g. "S"). Then sweep the grid: remaining "O" -> "X",
"S" -> "O". Use an iterative stack to avoid recursion limits.

Run: python3 surrounded_regions.py
"""


def solve(board: list) -> list:
    raise NotImplementedError


def _run_tests():
    b = [list("XXXX"), list("XOOX"), list("XXOX"), list("XOXX")]
    out = solve(b)
    assert out is b
    assert out == [list("XXXX"), list("XXXX"), list("XXXX"), list("XOXX")]
    assert solve([list("O")]) == [list("O")]
    assert solve([list("X")]) == [list("X")]
    assert solve([]) == []
    big = [list("OOOO"), list("OXXO"), list("OXXO"), list("OOOO")]
    assert solve([r[:] for r in big]) == big
    inner = [list("XXXXX"), list("XOOOX"), list("XOXOX"), list("XOOOX"), list("XXXXX")]
    assert solve([r[:] for r in inner]) == [list("XXXXX")] * 5
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
