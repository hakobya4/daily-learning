"""
Day 40, Task 9 -- CS fundamentals: unique paths with obstacles (DP).

THE PROBLEM
------------
A robot starts at the top-left of a grid and wants the bottom-right, moving
only right or down. grid[r][c] == 1 is an obstacle (cannot step there), 0 is
free. Return the number of distinct paths (0 if start or goal is blocked).

  unique_paths([[0,0,0],[0,1,0],[0,0,0]]) -> 2

HOW TO WORK THROUGH THIS
-------------------------
dp[r][c] = dp[r-1][c] + dp[r][c-1] on free cells, 0 on obstacles. You can
compress to a single row. Handle an empty grid and a blocked start.

Run: python3 unique_paths_obstacles.py
"""


def unique_paths(grid: list) -> int:
    if not grid or not grid[0] or grid[0][0] == 1:
        return 0
    cols = len(grid[0])
    dp = [0] * cols
    dp[0] = 1
    for row in grid:
        for c in range(cols):
            if row[c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]
    return dp[-1]


def _run_tests():
    assert unique_paths([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert unique_paths([[0, 1], [0, 0]]) == 1
    assert unique_paths([[1, 0], [0, 0]]) == 0
    assert unique_paths([[0, 0], [0, 1]]) == 0
    assert unique_paths([[0]]) == 1
    assert unique_paths([[1]]) == 0
    assert unique_paths([]) == 0
    assert unique_paths([[0, 0, 0, 0]]) == 1
    assert unique_paths([[0, 0, 1, 0]]) == 0
    assert unique_paths([[0] * 7 for _ in range(3)]) == 28
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
