"""
Day 42, Task 2 -- Python: two pointers on a sorted array.

THE PROBLEM
------------
sorted_squares(nums) -> given a list of ints sorted in non-decreasing order
(may contain negatives), return the squares, also sorted, in O(n) time with
two pointers (no sorting the result).

pair_with_sum(nums, target) -> nums sorted; return the (i, j) with i < j and
nums[i] + nums[j] == target, or None. Must be O(n) and O(1) extra space.
If several pairs exist, return the one with the smallest i.

Run: python3 sorted_squares.py
"""


def sorted_squares(nums):
    n = len(nums)
    res = [0] * n
    lo, hi = 0, n - 1
    for pos in range(n - 1, -1, -1):
        if abs(nums[lo]) > abs(nums[hi]):
            res[pos] = nums[lo] ** 2
            lo += 1
        else:
            res[pos] = nums[hi] ** 2
            hi -= 1
    return res


def pair_with_sum(nums, target):
    # Moving both pointers inward finds the pair with the smallest i first:
    # any pair (i, j) is only skipped when i or j can't be part of a solution.
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        total = nums[lo] + nums[hi]
        if total == target:
            return (lo, hi)
        if total < target:
            lo += 1
        else:
            hi -= 1
    return None


def _run_tests():
    assert sorted_squares([]) == []
    assert sorted_squares([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]
    assert sorted_squares([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
    assert sorted_squares([-5, -4]) == [16, 25]
    assert sorted_squares([2]) == [4]
    assert pair_with_sum([2, 7, 11, 15], 9) == (0, 1)
    assert pair_with_sum([1, 2, 3, 4, 6], 6) == (1, 3)
    assert pair_with_sum([1, 2, 3], 100) is None
    assert pair_with_sum([], 1) is None
    assert pair_with_sum([3], 6) is None
    assert pair_with_sum([-3, 0, 3], 0) == (0, 2)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
