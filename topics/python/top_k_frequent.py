"""
Day 7, Task 4 -- Python: top-k frequent elements.

THE PROBLEM
------------
Write top_k_frequent(items: list, k: int) -> list that returns the k
MOST FREQUENT items from `items`, most frequent first. On a tie in
count, break it by FIRST-APPEARANCE order in the original list (the
item that showed up earliest among the tied ones comes first). If
there are fewer than k distinct items, just return all of them.

This is a nice contrast to Day 6's min-heap task: there you built a
heap from scratch; here the point is using the standard library well
-- collections.Counter for the counting, instead of hand-rolling a
tally dict.

HOW TO WORK THROUGH THIS
-------------------------
collections.Counter(items) gives you counts. A plain dict (and
Counter, which is a dict subclass) in modern Python remembers
FIRST-INSERTION order of its keys -- so counter.items() already comes
back in first-appearance order. sorted() is stable, so if you sort
counter.items() by count descending ONLY (sorted(counter.items(),
key=lambda pair: -pair[1])), ties automatically keep that
first-appearance order without you doing anything extra for it. Take
the first k, and pull out just the item from each (item, count) pair.

Run: python3 top_k_frequent.py
"""

from collections import Counter


def top_k_frequent(items: list, k: int) -> list:
    # TODO: Counter(items) to count, then a STABLE sort by count
    # descending, then take the first k items (not counts).
    raise NotImplementedError


def _run_tests() -> None:
    items = ["a", "b", "a", "c", "b", "a", "d"]
    # counts: a=3, b=2, c=1, d=1 -- c appears before d, so on a tie
    # for last place, c should win.
    assert top_k_frequent(items, 1) == ["a"]
    assert top_k_frequent(items, 2) == ["a", "b"]
    assert top_k_frequent(items, 3) == ["a", "b", "c"]
    assert top_k_frequent(items, 4) == ["a", "b", "c", "d"]

    # k larger than the number of distinct items -- just return them all.
    assert top_k_frequent(items, 10) == ["a", "b", "c", "d"]

    # empty input
    assert top_k_frequent([], 3) == []

    print("All top_k_frequent tests passed.")


if __name__ == "__main__":
    _run_tests()
