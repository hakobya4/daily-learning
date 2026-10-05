"""
Day 14, Task 8 -- CS fundamentals: grid flood fill (number of islands).

THE PROBLEM
------------
A grid is a list of equal-length strings of '1' (land) and '0' (water).
Cells connect horizontally and vertically (NOT diagonally).

    count_islands(["11000",
                   "11000",
                   "00100",
                   "00011"])  ->  3

    largest_island(grid) -> area (number of cells) of the biggest island,
                            0 if there is no land.

Both must work on a 300 x 300 all-land grid without hitting Python's
recursion limit, so use an explicit stack or a queue (BFS/DFS), not
plain recursion. Do not mutate the caller's grid.

HOW TO WORK THROUGH THIS
-------------------------
Scan every cell; when you find unvisited land, flood-fill it with a
visited set and count one island (and its size).

Run: python3 islands.py
"""


def _island_sizes(grid: list[str]) -> list[int]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    seen = [[False] * cols for _ in range(rows)]
    sizes = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or seen[r][c]:
                continue
            seen[r][c] = True
            stack = [(r, c)]
            area = 0
            while stack:
                y, x = stack.pop()
                area += 1
                for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                    if 0 <= ny < rows and 0 <= nx < cols and \
                            grid[ny][nx] == "1" and not seen[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((ny, nx))
            sizes.append(area)
    return sizes


def count_islands(grid: list[str]) -> int:
    return len(_island_sizes(grid))


def largest_island(grid: list[str]) -> int:
    sizes = _island_sizes(grid)
    return max(sizes) if sizes else 0


def _run_tests() -> None:
    g = ["11000", "11000", "00100", "00011"]
    assert count_islands(g) == 3
    assert largest_island(g) == 4
    assert g == ["11000", "11000", "00100", "00011"]
    assert count_islands([]) == 0
    assert largest_island([]) == 0
    assert count_islands(["000", "000"]) == 0
    assert largest_island(["000", "000"]) == 0
    assert count_islands(["101", "010", "101"]) == 5  # diagonals do not join
    assert largest_island(["111", "010", "010"]) == 5
    big = ["1" * 300] * 300
    assert count_islands(big) == 1
    assert largest_island(big) == 90000
    snake = []
    for r in range(101):
        snake.append("1" * 101 if r % 2 == 0 else ("0" * 100 + "1" if r % 4 == 1 else "1" + "0" * 100))
    assert count_islands(snake) == 1
    print("All islands tests passed.")


if __name__ == "__main__":
    _run_tests()
