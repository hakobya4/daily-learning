"""
Day 28, Task 10 -- CS fundamentals: rod cutting (dynamic programming).

THE PROBLEM
------------
prices[i] is the price of a rod piece of length i + 1. rod_cutting(prices,
n) returns the maximum total revenue obtainable by cutting a rod of length
n into integer-length pieces (any number of cuts, pieces may repeat).
Pieces longer than len(prices) cannot be sold. n == 0 -> 0.

  rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8) -> 22   (2 + 6)
  rod_cutting([3, 5, 8, 9, 10, 17, 17, 20], 8) -> 24   (eight pieces of length 1)

Also write rod_cutting_pieces(prices, n) -> list of piece lengths (sorted
descending) that achieve the optimum; ties may be broken any way, but the
pieces must sum to n and their prices must add up to the optimum.

HOW TO WORK THROUGH THIS
-------------------------
best[j] = max over k in 1..min(j, len(prices)) of prices[k-1] + best[j-k].
Remember the chosen first cut per j to rebuild the pieces.

Run: python3 rod_cutting.py
"""


def rod_cutting(prices: list, n: int) -> int:
    raise NotImplementedError


def rod_cutting_pieces(prices: list, n: int) -> list:
    raise NotImplementedError


def _run_tests():
    p = [1, 5, 8, 9, 10, 17, 17, 20]
    assert rod_cutting(p, 0) == 0
    assert rod_cutting(p, 1) == 1
    assert rod_cutting(p, 4) == 10
    assert rod_cutting(p, 8) == 22
    assert rod_cutting([3, 5, 8, 9, 10, 17, 17, 20], 8) == 24
    assert rod_cutting([2], 5) == 10            # only length-1 pieces exist
    assert rod_cutting(p, 12) == 34             # 6 + 6; the 8-piece limit forces cuts
    for prices, n in ((p, 8), (p, 7), (p, 12), ([2], 5)):
        pieces = rod_cutting_pieces(prices, n)
        assert sum(pieces) == n
        assert pieces == sorted(pieces, reverse=True)
        assert sum(prices[k - 1] for k in pieces) == rod_cutting(prices, n)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
