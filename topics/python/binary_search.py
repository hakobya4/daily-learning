"""
Day 1 — Python / CS fundamentals: binary search.

THE PROBLEM
------------
Given a sorted list `nums` and a `target` value, return the index of
`target` in `nums`, or -1 if it isn't present.

Do it in O(log n) time instead of the obvious O(n) linear scan: since the
list is sorted, you can look at the middle element and immediately throw
away half the remaining search space, based on whether the target is
smaller or larger than that middle element. Repeat on the half that's
left until you either find it or run out of room to search.

Implement BOTH:
  1. binary_search_iterative  — using a while loop and lo/hi pointers.
  2. binary_search_recursive  — same logic, expressed recursively.

Watch out for the classic off-by-one bugs:
  - loop condition should be `lo <= hi`, not `lo < hi` (or you'll miss
    the case where the target is the very last candidate).
  - after checking the middle, move to `mid + 1` / `mid - 1`, not `mid`
    (reusing `mid` itself is the #1 cause of infinite loops here).

HOW TO WORK THROUGH THIS
-------------------------
Run this file directly: `python3 binary_search.py`
It currently fails immediately (NotImplementedError) — that's expected.
Fill in the two functions below until `_run_tests()` prints
"All binary search tests passed." Don't peek at a reference solution
first; get stuck, think about it, and only look things up once you've
genuinely tried.
"""

from __future__ import annotations


def binary_search_iterative(nums: list[int], target: int) -> int:
    """Return the index of `target` in sorted `nums`, or -1 if absent.

    Iterative version — O(log n) time, O(1) extra space.
    """
    # TODO: implement using a while loop with lo/hi pointers.
    raise NotImplementedError


def binary_search_recursive(nums: list[int], target: int, lo: int = 0, hi: int | None = None) -> int:
    """Same contract as above, but recursive — O(log n) time, O(log n)
    call-stack space (each call halves the range until it terminates).
    """
    # TODO: implement recursively. `hi` defaults to len(nums) - 1 on the
    # first call — handle that before doing anything else.
    raise NotImplementedError


def _run_tests() -> None:
    cases = [
        # (sorted list, target, expected index)
        ([], 5, -1),
        ([5], 5, 0),
        ([5], 3, -1),
        ([1, 3, 5, 7, 9, 11], 1, 0),
        ([1, 3, 5, 7, 9, 11], 11, 5),
        ([1, 3, 5, 7, 9, 11], 7, 3),
        ([1, 3, 5, 7, 9, 11], 4, -1),
        ([1, 3, 5, 7, 9, 11], 12, -1),
        ([2, 2, 2, 2], 2, None),  # duplicates: just needs *a* valid index
    ]

    for nums, target, expected in cases:
        for fn in (binary_search_iterative, binary_search_recursive):
            got = fn(nums, target)
            if expected is None:
                assert nums[got] == target if got != -1 else target not in nums, (
                    f"{fn.__name__}({nums!r}, {target!r}) -> {got!r} is not a valid match"
                )
            else:
                assert got == expected, (
                    f"{fn.__name__}({nums!r}, {target!r}) -> {got!r}, expected {expected!r}"
                )

    print("All binary search tests passed.")


if __name__ == "__main__":
    _run_tests()
