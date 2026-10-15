"""
Day 24, Task 4 -- Python: generate an n x n spiral matrix.

THE PROBLEM
------------
spiral_generate(n) returns an n x n list of lists filled with 1..n*n in
clockwise spiral order starting at the top-left.

  spiral_generate(3) == [[1, 2, 3],
                         [8, 9, 4],
                         [7, 6, 5]]

spiral_generate(0) == []. Raise ValueError if n is negative.

HOW TO WORK THROUGH THIS
-------------------------
Keep a direction (right, down, left, up) and turn clockwise whenever the
next cell is off the board or already filled. Or peel layers with
top/bottom/left/right boundaries that shrink.

Run: python3 spiral_generate.py
"""


def spiral_generate(n: int) -> list:
    if n < 0:
        raise ValueError("n must be non-negative")
    grid = [[0] * n for _ in range(n)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r = c = d = 0
    for k in range(1, n * n + 1):
        grid[r][c] = k
        dr, dc = dirs[d]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < n) or grid[nr][nc]:
            d = (d + 1) % 4
            dr, dc = dirs[d]
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return grid


def _run_tests():
    assert spiral_generate(0) == []
    assert spiral_generate(1) == [[1]]
    assert spiral_generate(2) == [[1, 2], [4, 3]]
    assert spiral_generate(3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
    assert spiral_generate(4) == [
        [1, 2, 3, 4],
        [12, 13, 14, 5],
        [11, 16, 15, 6],
        [10, 9, 8, 7],
    ]
    m = spiral_generate(7)
    assert sorted(x for row in m for x in row) == list(range(1, 50))
    try:
        spiral_generate(-2)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
