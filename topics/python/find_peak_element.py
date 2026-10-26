"""
Day 35, Task 3 -- Python: find a peak element in O(log n).

THE PROBLEM
------------
A peak is an element strictly greater than its neighbours. Given a list
nums where adjacent elements are never equal, return the INDEX of ANY peak.
Treat nums[-1] and nums[len] as negative infinity, so the ends can be peaks.
Must run in O(log n) -- no linear scan.

  [1,2,3,1]        -> 2
  [1,2,1,3,5,6,4]  -> 1 or 5 (either is accepted)

HOW TO WORK THROUGH THIS
-------------------------
Binary search with lo, hi. Compare nums[mid] with nums[mid+1]: if it is
smaller, a peak lies to the right (lo = mid+1); otherwise a peak lies at
mid or to the left (hi = mid). Stop when lo == hi.

Run: python3 find_peak_element.py
"""


def find_peak_element(nums: list) -> int:
    raise NotImplementedError


def _is_peak(nums, i):
    left = nums[i - 1] if i > 0 else float("-inf")
    right = nums[i + 1] if i < len(nums) - 1 else float("-inf")
    return nums[i] > left and nums[i] > right


def _run_tests():
    cases = [
        [1],
        [1, 2],
        [2, 1],
        [1, 2, 3, 1],
        [1, 2, 1, 3, 5, 6, 4],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        list(range(1000)) + list(range(998, 0, -1)),
    ]
    for nums in cases:
        i = find_peak_element(nums)
        assert 0 <= i < len(nums) and _is_peak(nums, i), (nums[:10], i)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
