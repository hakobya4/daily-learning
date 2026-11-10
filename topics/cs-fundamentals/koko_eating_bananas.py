"""
Day 51, Task 7 -- CS fundamentals: binary search on the answer (Koko eating bananas).

THE PROBLEM
------------
min_eating_speed(piles, h): there are piles[i] bananas in pile i. Koko eats at a speed of k
bananas/hour, choosing one pile per hour; if the pile has fewer than k bananas she finishes
it and does nothing else that hour. Return the minimum integer k so that she finishes all
piles within h hours (h >= len(piles)).
Examples: ([3, 6, 7, 11], 8) -> 4, ([30, 11, 23, 4, 20], 5) -> 30.
Hint: hours(k) = sum(ceil(p / k)) is non-increasing in k, so binary search k in [1, max(piles)].

Run: python3 koko_eating_bananas.py
"""


def min_eating_speed(piles, h):
    raise NotImplementedError


def _run_tests():
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
    assert min_eating_speed([1], 1) == 1
    assert min_eating_speed([1000000000], 2) == 500000000
    assert min_eating_speed([312884470], 312884469) == 2
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
