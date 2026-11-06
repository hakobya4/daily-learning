"""
Day 47, Task 1 -- Python: minimum arrows to burst all balloons (greedy intervals).

THE PROBLEM
------------
balloons is a list of [x_start, x_end] horizontal diameters. An arrow shot
vertically at x bursts every balloon with x_start <= x <= x_end (touching
endpoints count). min_arrows(balloons) returns the minimum number of arrows
needed to burst them all. Do not mutate the input. Empty list -> 0.
Hint: sort by end; shoot at the current end; start a new arrow only when the
next balloon starts after that end.

Run: python3 min_arrows_balloons.py
"""


def min_arrows(balloons):
    raise NotImplementedError


def _run_tests():
    assert min_arrows([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert min_arrows([[1, 2], [3, 4], [5, 6], [7, 8]]) == 4
    assert min_arrows([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2
    assert min_arrows([]) == 0
    assert min_arrows([[-2147483648, 2147483647]]) == 1
    assert min_arrows([[1, 5], [2, 3], [4, 6]]) == 2
    assert min_arrows([[1, 10], [2, 9], [3, 8]]) == 1
    orig = [[3, 4], [1, 2]]
    min_arrows(orig)
    assert orig == [[3, 4], [1, 2]]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
