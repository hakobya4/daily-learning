"""
Day 43, Task 3 -- Python: first missing positive integer.

THE PROBLEM
------------
first_missing_positive(nums) -> the smallest positive integer (>= 1) that
does not appear in nums. Aim for O(n) time and O(1) extra space (you may
mutate nums): place each value v in 1..n at index v-1 by swapping ("cyclic
sort"), then scan for the first index i where nums[i] != i+1.
  [1, 2, 0] -> 3     [3, 4, -1, 1] -> 2     [7, 8, 9, 11, 12] -> 1
Beware duplicates (they can cause infinite swap loops).

Run: python3 first_missing_positive.py
"""


def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1


def _run_tests():
    assert first_missing_positive([1, 2, 0]) == 3
    assert first_missing_positive([3, 4, -1, 1]) == 2
    assert first_missing_positive([7, 8, 9, 11, 12]) == 1
    assert first_missing_positive([]) == 1
    assert first_missing_positive([1]) == 2
    assert first_missing_positive([2, 1]) == 3
    assert first_missing_positive([1, 1]) == 2
    assert first_missing_positive([2, 2, 2, 1, 1, 3]) == 4
    assert first_missing_positive(list(range(1, 1001))) == 1001
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
