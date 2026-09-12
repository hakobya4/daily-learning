"""
Day 1 — Python / CS fundamentals: binary search.

What I'm practicing: searching a sorted sequence in O(log n) instead of
O(n) by halving the search space each step, and being careful with the
classic off-by-one bugs (mid calculation, updating lo/hi correctly).

Includes both an iterative and a recursive version, plus a tiny
hand-rolled test harness (no pytest dependency) so the file can just be
run directly with `python3 binary_search.py`.
"""

from __future__ import annotations


def binary_search_iterative(nums: list[int], target: int) -> int:
    """Return the index of `target` in sorted `nums`, or -1 if absent.

    Iterative version — O(log n) time, O(1) extra space.
    """
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoids overflow in other languages;
        # in Python it's not strictly needed, but it's the habit worth
        # building since it's required in languages with fixed-width ints.

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


def binary_search_recursive(nums: list[int], target: int, lo: int = 0, hi: int | None = None) -> int:
    """Same contract as above, but recursive — O(log n) time, O(log n)
    call-stack space (each call halves the range until it terminates).
    """
    if hi is None:
        hi = len(nums) - 1

    if lo > hi:
        return -1

    mid = lo + (hi - lo) // 2

    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return binary_search_recursive(nums, target, mid + 1, hi)
    else:
        return binary_search_recursive(nums, target, lo, mid - 1)


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
