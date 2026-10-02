"""
Day 9, Task 10 -- Python: maximum subarray sum (replaces the open-source rep).

THE PROBLEM
------------
Write max_subarray(nums: list[int]) -> int returning the largest sum of
any non-empty contiguous subarray. Raise ValueError for an empty list.

  [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> 6   (subarray [4, -1, 2, 1])

Kadane's algorithm: O(n) time, O(1) space.

Run: python3 max_subarray.py
"""


def max_subarray(nums: list[int]) -> int:
    if not nums:
        raise ValueError("nums must be non-empty")
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def _run_tests() -> None:
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray([1]) == 1
    assert max_subarray([5, 4, -1, 7, 8]) == 23
    assert max_subarray([-3, -1, -2]) == -1
    assert max_subarray([0, 0]) == 0
    try:
        max_subarray([])
        assert False, "should reject empty list"
    except ValueError:
        pass
    print("All max_subarray tests passed.")


if __name__ == "__main__":
    _run_tests()
