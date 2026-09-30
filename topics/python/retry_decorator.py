"""
Day 9, Task 4 -- Python: a retry decorator.

THE PROBLEM
------------
Write retry(times: int, exceptions: tuple = (Exception,)) -- a
decorator FACTORY. A function wrapped with @retry(3) is called; if it
raises one of `exceptions` it is called again, up to `times` TOTAL
attempts. If an attempt succeeds, return its value. If the last
attempt still fails, let that exception propagate. Exceptions NOT in
`exceptions` must propagate immediately with no retry. Use
functools.wraps so the wrapped function keeps its __name__.

HOW TO WORK THROUGH THIS
-------------------------
Three nested functions: retry(times, exceptions) -> decorator(func) ->
wrapper(*args, **kwargs). Loop over attempts inside wrapper; re-raise
on the final attempt.

Run: python3 retry_decorator.py
"""
import functools  # noqa: F401  (you'll want functools.wraps)


def retry(times: int, exceptions: tuple = (Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
        return wrapper
    return decorator


def _run_tests() -> None:
    calls = {"n": 0}

    @retry(3)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("not yet")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3
    assert flaky.__name__ == "flaky"

    calls2 = {"n": 0}

    @retry(2)
    def always_fails():
        calls2["n"] += 1
        raise RuntimeError("boom")

    try:
        always_fails()
        assert False, "should have raised"
    except RuntimeError:
        pass
    assert calls2["n"] == 2, calls2

    calls3 = {"n": 0}

    @retry(5, exceptions=(KeyError,))
    def wrong_kind():
        calls3["n"] += 1
        raise TypeError("not retried")

    try:
        wrong_kind()
        assert False, "should have raised"
    except TypeError:
        pass
    assert calls3["n"] == 1, calls3

    @retry(2)
    def adds(a, b=0):
        return a + b

    assert adds(1, b=2) == 3
    print("All retry_decorator tests passed.")


if __name__ == "__main__":
    _run_tests()
