"""
Day 32, Task 3 -- Python: maximum product subarray.

THE PROBLEM
------------
Given a list of integers nums (non-empty), return the largest product of
any contiguous, non-empty subarray.

  [2, 3, -2, 4]   -> 6
  [-2, 0, -1]     -> 0
  [-2, 3, -4]     -> 24
  [-3]            -> -3

HOW TO WORK THROUGH THIS
-------------------------
A negative number can flip the smallest product into the largest, so keep
BOTH the max and the min product of a subarray ending at the current index.
Update both with (x, x*max_prev, x*min_prev) at every step.

Run: python3 max_product_subarray.py
"""


def max_product(nums: list) -> int:
    best = cur_max = cur_min = nums[0]
    for x in nums[1:]:
        cands = (x, x * cur_max, x * cur_min)
        cur_max, cur_min = max(cands), min(cands)
        best = max(best, cur_max)
    return best


def _run_tests():
    assert max_product([2, 3, -2, 4]) == 6
    assert max_product([-2, 0, -1]) == 0
    assert max_product([-2, 3, -4]) == 24
    assert max_product([-3]) == -3
    assert max_product([0, 2]) == 2
    assert max_product([-2, -3, -4]) == 12
    assert max_product([2, -5, -2, -4, 3]) == 24
    assert max_product([1, 1, 1]) == 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
