"""
Day 13, Task 10 -- Python: largest rectangle in a histogram.

THE PROBLEM
------------
Given bar heights (non-negative ints, each bar has width 1), return the
area of the largest rectangle that fits entirely inside the histogram.

    [2, 1, 5, 6, 2, 3]  ->  10   (bars 5 and 6, height 5, width 2)

Also implement largest_rectangle(heights) -> (area, left, right) where
left/right are the inclusive bar indices of the best rectangle (if
several tie, return the one with the smallest left index; empty input
-> (0, -1, -1)).

Aim for O(n) with a monotonic stack of indices (a brute-force O(n^2)
version is fine as a first step to cross-check).

Run: python3 histogram_area.py
"""


def max_area(heights: list[int]) -> int:
    return largest_rectangle(heights)[0]


def largest_rectangle(heights: list[int]) -> tuple[int, int, int]:
    if not heights:
        return (0, -1, -1)
    best = (0, -1, -1)
    stack: list[int] = []  # indices with increasing heights
    n = len(heights)
    for i in range(n + 1):
        cur = heights[i] if i < n else -1
        while stack and heights[stack[-1]] >= cur:
            h = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            right = i - 1
            cand = (h * (right - left + 1), left, right)
            if cand[0] > best[0] or (cand[0] == best[0] and best[0] > 0 and cand[1] < best[1]):
                best = cand
        stack.append(i)
    if best[0] == 0:
        return (0, 0, 0)
    return best


def _run_tests() -> None:
    assert max_area([]) == 0
    assert max_area([0]) == 0
    assert max_area([5]) == 5
    assert max_area([2, 1, 5, 6, 2, 3]) == 10
    assert max_area([2, 4]) == 4
    assert max_area([1, 1, 1, 1]) == 4
    assert max_area([6, 5, 4, 3, 2, 1]) == 12
    assert largest_rectangle([]) == (0, -1, -1)
    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == (10, 2, 3)
    assert largest_rectangle([1, 1, 1, 1]) == (4, 0, 3)
    assert largest_rectangle([3, 0, 3]) == (3, 0, 0)
    import random
    random.seed(13)
    for _ in range(200):
        h = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
        brute = 0
        for i in range(len(h)):
            lo = h[i]
            for j in range(i, len(h)):
                lo = min(lo, h[j])
                brute = max(brute, lo * (j - i + 1))
        assert max_area(h) == brute, h
        assert largest_rectangle(h)[0] == brute, h
    print("All histogram_area tests passed.")


if __name__ == "__main__":
    _run_tests()
