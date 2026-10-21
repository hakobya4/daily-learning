"""
Day 31, Task 2 -- Python: longest mountain in an array.

THE PROBLEM
------------
A mountain is a contiguous subarray of length >= 3 that strictly increases
to a single peak and then strictly decreases. longest_mountain(arr) returns
the length of the longest mountain, or 0 if there is none.

  [2,1,4,7,3,2,5] -> 5   (1,4,7,3,2)
  [2,2,2]         -> 0
  [1,2,3]         -> 0   (no descent)

HOW TO WORK THROUGH THIS
-------------------------
One pass, O(1) space: for each peak i (arr[i-1] < arr[i] > arr[i+1]) walk
left while strictly decreasing and right while strictly decreasing, then
jump i past the right end. Or precompute up[]/down[] run lengths.

Run: python3 longest_mountain.py
"""


def longest_mountain(arr: list) -> int:
    n = len(arr)
    best = 0
    i = 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:
            lo = i - 1
            while lo > 0 and arr[lo - 1] < arr[lo]:
                lo -= 1
            hi = i + 1
            while hi < n - 1 and arr[hi] > arr[hi + 1]:
                hi += 1
            best = max(best, hi - lo + 1)
            i = hi
        else:
            i += 1
    return best


def _run_tests():
    assert longest_mountain([2, 1, 4, 7, 3, 2, 5]) == 5
    assert longest_mountain([2, 2, 2]) == 0
    assert longest_mountain([]) == 0
    assert longest_mountain([1, 2, 3]) == 0
    assert longest_mountain([3, 2, 1]) == 0
    assert longest_mountain([1, 3, 2]) == 3
    assert longest_mountain([0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]) == 11
    assert longest_mountain([2, 3, 3, 2]) == 0
    assert longest_mountain([1, 2, 1, 2, 3, 2, 1]) == 5
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
