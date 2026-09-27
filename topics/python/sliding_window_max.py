"""
Day 6, Task 4 -- Python: maximum of every sliding window.

THE PROBLEM
------------
Given a list of integers `nums` and a window size `k`, return a list
containing the MAXIMUM value in every contiguous window of size k as
it slides from left to right across `nums`. The result has
len(nums) - k + 1 elements.

Example: sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
         -> [3, 3, 5, 5, 6, 7]
(windows: [1,3,-1]->3, [3,-1,-3]->3, [-1,-3,5]->5, [-3,5,3]->5,
 [5,3,6]->6, [3,6,7]->7)

The obvious approach (scan each window for its max) is O(n*k). The
real point of this exercise is the O(n) approach using a deque of
INDICES.

HOW TO WORK THROUGH THIS
-------------------------
Keep a deque of indices into `nums`, always kept in DECREASING order
of their values (the index of the current window's max is always at
the front). For each new index i: (1) pop indices off the FRONT if
they've fallen out of the window (index <= i - k); (2) pop indices off
the BACK as long as their value is <= nums[i] (they can never be the
max again, since nums[i] is later AND at least as big); (3) append i
to the back. Once i >= k - 1, the window is full -- record
nums[deque[0]] as this window's max.

Run: python3 sliding_window_max.py
"""

from collections import deque


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    dq = deque()  # indices, values decreasing left to right
    result = []
    for i, num in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result


def _run_tests() -> None:
    cases = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([4, 3, 2, 1], 2, [4, 3, 2]),
        ([9], 1, [9]),
        ([1, 1, 1, 1], 2, [1, 1, 1]),
        ([5, 4, 3, 2, 1], 5, [5]),
    ]
    for nums, k, expected in cases:
        got = sliding_window_max(nums, k)
        assert got == expected, f"sliding_window_max({nums!r}, {k!r}) -> {got!r}, expected {expected!r}"
    print("All sliding_window_max tests passed.")


if __name__ == "__main__":
    _run_tests()
