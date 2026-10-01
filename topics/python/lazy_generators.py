"""
Day 10, Task 3 -- Python: lazy generators.

THE PROBLEM
------------
Implement three GENERATOR functions (use `yield`; do not build the whole
result list up front). They must work on infinite iterators.

  chunked(iterable, n)   -> yields lists of up to n items:
                            chunked("abcde", 2) -> ['a','b'], ['c','d'], ['e']
  pairwise(iterable)     -> yields overlapping pairs (tuples):
                            pairwise([1,2,3,4]) -> (1,2), (2,3), (3,4)
                            fewer than 2 items -> yields nothing
  take_while_sum(iterable, limit)
                         -> yields items from the front while the running
                            total stays <= limit; stops before the item
                            that would push it over.

Raise ValueError (when the generator is first advanced is fine) if n < 1
in chunked.

HOW TO WORK THROUGH THIS
-------------------------
Call iter() on the input once. For chunked, itertools.islice on the
iterator is handy; for pairwise, remember the previous item.

Run: python3 lazy_generators.py
"""
import itertools  # noqa: F401


def chunked(iterable, n):
    if n < 1:
        raise ValueError("n must be >= 1")
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def pairwise(iterable):
    it = iter(iterable)
    try:
        prev = next(it)
    except StopIteration:
        return
    for item in it:
        yield (prev, item)
        prev = item


def take_while_sum(iterable, limit):
    total = 0
    for item in iterable:
        total += item
        if total > limit:
            return
        yield item


def _run_tests() -> None:
    assert list(chunked("abcde", 2)) == [["a", "b"], ["c", "d"], ["e"]]
    assert list(chunked([], 3)) == []
    assert list(chunked(range(6), 3)) == [[0, 1, 2], [3, 4, 5]]
    try:
        list(chunked([1], 0))
        assert False, "n < 1 must raise"
    except ValueError:
        pass
    # laziness: works on an infinite iterator
    first = next(chunked(itertools.count(), 4))
    assert first == [0, 1, 2, 3]

    assert list(pairwise([1, 2, 3, 4])) == [(1, 2), (2, 3), (3, 4)]
    assert list(pairwise([1])) == []
    assert list(pairwise([])) == []
    assert next(pairwise(itertools.count())) == (0, 1)

    assert list(take_while_sum([1, 2, 3, 4], 6)) == [1, 2, 3]
    assert list(take_while_sum([5, 1], 4)) == []
    assert list(take_while_sum(itertools.count(1), 10)) == [1, 2, 3, 4]
    print("All lazy_generators tests passed.")


if __name__ == "__main__":
    _run_tests()
