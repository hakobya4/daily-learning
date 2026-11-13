"""
Day 54, Task 1 -- Python: online stock span (monotonic stack inside a class).

THE PROBLEM
------------
Implement StockSpanner with one method, next(price) -> int, called once per day with that
day's price. It returns the SPAN of today's price: the number of consecutive days, ending
today and going backwards, on which the price was <= today's price (today counts, so the
span is always >= 1).

Example: prices 100, 80, 60, 70, 60, 75, 85 give spans 1, 1, 1, 2, 1, 4, 6.

A naive backwards scan is O(n) per call (O(n^2) total for an increasing series). Aim for
amortised O(1) per call.
Hint: keep a stack of (price, span) pairs with STRICTLY decreasing prices. When a new price
arrives, pop every pair whose price is <= the new price and add its span to the new span,
then push (price, span). Each price is pushed and popped at most once.
Raise ValueError for a negative price (prices of 0 are allowed).

Run: python3 online_stock_span.py
"""


class StockSpanner:
    def __init__(self):
        raise NotImplementedError

    def next(self, price):
        raise NotImplementedError


def _spans(prices):
    s = StockSpanner()
    return [s.next(p) for p in prices]


def _run_tests():
    assert _spans([100, 80, 60, 70, 60, 75, 85]) == [1, 1, 1, 2, 1, 4, 6]
    assert _spans([5]) == [1]
    assert _spans([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert _spans([5, 4, 3, 2, 1]) == [1, 1, 1, 1, 1]
    assert _spans([7, 7, 7, 7]) == [1, 2, 3, 4]          # equal prices count (<=)
    assert _spans([3, 1, 2, 0, 4]) == [1, 1, 2, 1, 5]
    assert _spans([0, 0, 1]) == [1, 2, 3]

    # Increasing series of 200k prices must finish quickly (amortised O(1)).
    big = _spans(range(200_000))
    assert big[-1] == 200_000 and big[0] == 1

    # Independent instances do not share state.
    a, b = StockSpanner(), StockSpanner()
    assert a.next(10) == 1
    assert b.next(1) == 1
    assert a.next(20) == 2
    assert b.next(0) == 1

    try:
        StockSpanner().next(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative price must raise ValueError")

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
