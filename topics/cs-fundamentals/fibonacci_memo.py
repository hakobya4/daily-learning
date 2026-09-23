"""
Day 3, Task 8 -- CS fundamentals: memoized Fibonacci.

THE PROBLEM
------------
Write two functions:

  fib_naive(n)  -- the textbook recursive definition, no caching.
                   Fine for small n, exponentially slow past ~n=30.
  fib_memo(n)   -- the same recursive definition, but caching results
                   in a dict so each n is only computed once.

Both should return the nth Fibonacci number (fib(0)=0, fib(1)=1,
fib(2)=1, fib(3)=2, ...).

HOW TO WORK THROUGH THIS
-------------------------
Write fib_naive first -- it's the direct translation of the
definition. Then write fib_memo: same shape, but check a cache dict
before recursing, and store the result before returning. Once both
work, uncomment the timing comparison at the bottom of _run_tests and
watch fib_naive get noticeably slow around n=30-32 while fib_memo
stays instant.

Run: python3 fibonacci_memo.py
"""


def fib_naive(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n: int, _cache: dict | None = None) -> int:
    if _cache is None:
        _cache = {}
    if n in _cache:
        return _cache[n]
    if n == 0:
        result = 0
    elif n == 1:
        result = 1
    else:
        result = fib_memo(n - 1, _cache) + fib_memo(n - 2, _cache)
    _cache[n] = result
    return result


def _run_tests() -> None:
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    for n, exp in enumerate(expected):
        assert fib_naive(n) == exp, f"fib_naive({n}) -> {fib_naive(n)}, expected {exp}"
        assert fib_memo(n) == exp, f"fib_memo({n}) -> {fib_memo(n)}, expected {exp}"

    # Uncomment once both work, to feel the difference:
    # import time
    # start = time.time(); fib_naive(30); print("naive:", time.time() - start)
    # start = time.time(); fib_memo(30); print("memo: ", time.time() - start)

    print("All fibonacci_memo tests passed.")


if __name__ == "__main__":
    _run_tests()
