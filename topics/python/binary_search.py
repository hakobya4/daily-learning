"""
Day 1 — Python / CS fundamentals: binary search.

"""

from __future__ import annotations


def binary_search_iterative(nums: list[int], target: int) -> int:
    lo = 0
    hi = len(nums) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        
        if nums[mid] == target:
            return mid  # Target found
        elif nums[mid] < target:
            lo = mid + 1  # Narrow search to the upper half
        else:
            hi = mid - 1  # Narrow search to the lower ha
    return -1
    raise NotImplementedError


def binary_search_recursive(nums: list[int], target: int, lo: int = 0, hi: int | None = None) -> int:
    if hi is None:
        hi = len(nums) - 1

    if lo > hi:
        return -1  # Target not found
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return binary_search_recursive(nums, target, lo=mid + 1, hi=hi)
    else:
        return binary_search_recursive(nums, target, lo=lo, hi=mid - 1)


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
