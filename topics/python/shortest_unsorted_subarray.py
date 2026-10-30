"""
Day 40, Task 3 -- Python: shortest unsorted continuous subarray.

THE PROBLEM
------------
Given a list of ints, find the shortest contiguous subarray that, if sorted
ascending, makes the WHOLE list sorted ascending. Return its length (0 if the
list is already sorted).

  shortest_unsorted([2, 6, 4, 8, 10, 9, 15]) -> 5   (sort [6,4,8,10,9])
  shortest_unsorted([1, 2, 3, 4]) -> 0

HOW TO WORK THROUGH THIS
-------------------------
O(n) two-pass idea: scan left to right tracking the running max; the last
index where nums[i] < running max is the right end. Scan right to left
tracking the running min; the last index where nums[i] > running min is the
left end. Duplicates need care (equal elements are fine where they are).

Run: python3 shortest_unsorted_subarray.py
"""


def shortest_unsorted(nums: list) -> int:
    n = len(nums)
    end = -1
    run_max = float("-inf")
    for i in range(n):
        if nums[i] < run_max:
            end = i
        else:
            run_max = nums[i]
    if end == -1:
        return 0
    start = 0
    run_min = float("inf")
    for i in range(n - 1, -1, -1):
        if nums[i] > run_min:
            start = i
        else:
            run_min = nums[i]
    return end - start + 1


def _run_tests():
    assert shortest_unsorted([2, 6, 4, 8, 10, 9, 15]) == 5
    assert shortest_unsorted([1, 2, 3, 4]) == 0
    assert shortest_unsorted([]) == 0
    assert shortest_unsorted([1]) == 0
    assert shortest_unsorted([2, 1]) == 2
    assert shortest_unsorted([1, 3, 2, 2, 2]) == 4
    assert shortest_unsorted([1, 2, 2, 2, 3]) == 0
    assert shortest_unsorted([5, 4, 3, 2, 1]) == 5
    assert shortest_unsorted([1, 2, 4, 5, 3]) == 3
    assert shortest_unsorted([1, 3, 5, 4, 2, 6, 7]) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
