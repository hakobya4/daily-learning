"""
Day 57, Task 1 -- Python: maximal all-ones rectangle in a binary matrix.

THE PROBLEM
------------
`grid` is a list of equal-length strings made of '0' and '1' (possibly an empty list,
or rows of length 0). Return the AREA of the largest axis-aligned rectangle that
contains only '1' cells.

Also implement best_rectangle(grid) -> (top, left, bottom, right) with INCLUSIVE
coordinates of one rectangle achieving the maximum area, or None if the grid has no
'1' at all. Any optimal rectangle is accepted; the tests check that it is all ones and
has the maximal area.

Example:
  grid = ["10100",
          "10111",
          "11111",
          "10010"]
  maximal_rectangle(grid) -> 6      (rows 1..2, columns 2..4)
  maximal_rectangle([])   -> 0
  maximal_rectangle(["0"]) -> 0

Hint: process row by row and keep `heights[c]` = number of consecutive '1's ending at
the current row in column c (reset to 0 on a '0'). Each row then becomes "largest
rectangle in a histogram", solvable in O(cols) with a monotonic increasing stack of
indices (push a sentinel height 0 at the end to flush the stack). Total O(rows * cols).
To recover the rectangle, remember (height, left, right, row) whenever the best area
improves -- when you pop index i with height h, its width spans from the index below it
on the stack + 1 up to the current index - 1.

Run: python3 maximal_rectangle.py
"""


def _scan(grid):
    """Return (best_area, rect) using row-by-row histograms + a monotonic stack."""
    if not grid or not grid[0]:
        return 0, None
    cols = len(grid[0])
    heights = [0] * cols
    best, rect = 0, None
    for row_idx, row in enumerate(grid):
        for c in range(cols):
            heights[c] = heights[c] + 1 if row[c] == "1" else 0
        stack = []  # indices with increasing heights
        for i in range(cols + 1):
            cur = heights[i] if i < cols else 0
            while stack and heights[stack[-1]] >= cur:
                h = heights[stack.pop()]
                left = stack[-1] + 1 if stack else 0
                right = i - 1
                area = h * (right - left + 1)
                if area > best:
                    best = area
                    rect = (row_idx - h + 1, left, row_idx, right)
            stack.append(i)
    return best, rect


def maximal_rectangle(grid):
    return _scan(grid)[0]


def best_rectangle(grid):
    return _scan(grid)[1]


def _brute(grid):
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    best = 0
    for t in range(R):
        for l in range(C):
            for b in range(t, R):
                for r in range(l, C):
                    if all(grid[i][j] == "1" for i in range(t, b + 1) for j in range(l, r + 1)):
                        best = max(best, (b - t + 1) * (r - l + 1))
    return best


def _check_rect(grid, rect, area):
    t, l, b, r = rect
    assert 0 <= t <= b < len(grid) and 0 <= l <= r < len(grid[0]), rect
    assert (b - t + 1) * (r - l + 1) == area, (rect, area)
    assert all(grid[i][j] == "1" for i in range(t, b + 1) for j in range(l, r + 1)), rect


def _run_tests():
    g = ["10100", "10111", "11111", "10010"]
    assert maximal_rectangle(g) == 6
    _check_rect(g, best_rectangle(g), 6)
    assert maximal_rectangle([]) == 0
    assert maximal_rectangle([""]) == 0
    assert maximal_rectangle(["0"]) == 0
    assert best_rectangle(["0"]) is None
    assert best_rectangle([]) is None
    assert maximal_rectangle(["1"]) == 1
    assert best_rectangle(["1"]) == (0, 0, 0, 0)
    assert maximal_rectangle(["111", "111"]) == 6
    assert maximal_rectangle(["01", "10"]) == 1
    assert maximal_rectangle(["1101", "1101", "1111"]) == 6

    import random
    rng = random.Random(57)
    for _ in range(300):
        R, C = rng.randint(1, 6), rng.randint(1, 6)
        p = rng.random()
        grid = ["".join("1" if rng.random() < p else "0" for _ in range(C)) for _ in range(R)]
        exp = _brute(grid)
        assert maximal_rectangle(grid) == exp, grid
        rect = best_rectangle(grid)
        if exp == 0:
            assert rect is None, grid
        else:
            _check_rect(grid, rect, exp)

    # O(rows * cols): 600 x 600 all ones must be fast.
    big = ["1" * 600] * 600
    assert maximal_rectangle(big) == 360_000
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
