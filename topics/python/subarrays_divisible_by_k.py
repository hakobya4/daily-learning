"""
Day 49, Task 1 -- Python: count subarrays whose sum is divisible by K.

THE PROBLEM
------------
Given a list of integers nums (may include negatives) and an integer k > 0,
subarrays_div_by_k(nums, k) returns the number of non-empty contiguous
subarrays whose sum is divisible by k.
Examples: ([4,5,0,-2,-3,1], 5) -> 7, ([5], 9) -> 0, ([0,0], 3) -> 3.
Hint: prefix sums + a counter of prefix % k. Python's % is already non-negative
for a positive k. Two equal remainders mean the slice between them sums to 0 mod k.

Run: python3 subarrays_divisible_by_k.py
"""


def subarrays_div_by_k(nums, k):
    raise NotImplementedError


def _run_tests():
    assert subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5) == 7
    assert subarrays_div_by_k([5], 9) == 0
    assert subarrays_div_by_k([0, 0], 3) == 3
    assert subarrays_div_by_k([], 4) == 0
    assert subarrays_div_by_k([-1, 2, 9], 2) == 2
    assert subarrays_div_by_k([3, 3, 3], 3) == 6
    assert subarrays_div_by_k([1, 2, 3], 1) == 6
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
