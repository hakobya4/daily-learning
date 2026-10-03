"""
Day 12, Task 10 -- Python: minimum path sum in a grid (DP).

THE PROBLEM
------------
min_path_sum(grid) takes a non-empty rectangular list of lists of
non-negative ints. Starting at the top-left cell, you may move only
RIGHT or DOWN to reach the bottom-right cell. Return the smallest
possible sum of the cell values along a path (both end cells included).

Also implement min_path(grid) -> list of (row, col) cells along one
optimal path, from start to end. If several paths tie, any is accepted;
the tests only check that the path is valid and its sum is optimal.

Raise ValueError for an empty grid or ragged rows.

HOW TO WORK THROUGH THIS
-------------------------
dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1]) with the first row
and column handled separately. For min_path, walk back from the end
choosing the cheaper predecessor and reverse.

Run: python3 min_path_sum.py
"""


def _dp(grid):
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("grid must be non-empty and rectangular")
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            best = 0
            if r and c:
                best = min(dp[r - 1][c], dp[r][c - 1])
            elif r:
                best = dp[r - 1][c]
            elif c:
                best = dp[r][c - 1]
            dp[r][c] = grid[r][c] + best
    return dp


def min_path_sum(grid):
    dp = _dp(grid)
    return dp[-1][-1]


def min_path(grid):
    dp = _dp(grid)
    r, c = len(grid) - 1, len(grid[0]) - 1
    path = [(r, c)]
    while (r, c) != (0, 0):
        if r == 0:
            c -= 1
        elif c == 0:
            r -= 1
        elif dp[r - 1][c] <= dp[r][c - 1]:
            r -= 1
        else:
            c -= 1
        path.append((r, c))
    path.reverse()
    return path


def _run_tests() -> None:
    g = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    assert min_path_sum(g) == 7
    assert min_path_sum([[5]]) == 5
    assert min_path_sum([[1, 2, 3]]) == 6
    assert min_path_sum([[1], [2], [3]]) == 6
    assert min_path_sum([[1, 2], [1, 1]]) == 3
    big = [[(r * 7 + c * 3) % 10 for c in range(6)] for r in range(5)]
    for grid in (g, big):
        p = min_path(grid)
        assert p[0] == (0, 0) and p[-1] == (len(grid) - 1, len(grid[0]) - 1)
        for (r1, c1), (r2, c2) in zip(p, p[1:]):
            assert (r2 - r1, c2 - c1) in ((0, 1), (1, 0))
        assert sum(grid[r][c] for r, c in p) == min_path_sum(grid)
    for bad in ([], [[]], [[1, 2], [3]]):
        try:
            min_path_sum(bad)
            assert False, f"should reject {bad!r}"
        except ValueError:
            pass
    print("All min_path_sum tests passed.")


if __name__ == "__main__":
    _run_tests()
