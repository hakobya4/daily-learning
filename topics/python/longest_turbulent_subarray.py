"""
Day 52, Task 10 -- Python: longest turbulent subarray (sliding window / DP).

THE PROBLEM
------------
max_turbulence_size(arr): a subarray arr[i..j] is turbulent if the comparison sign flips
between every adjacent pair, e.g. a > b < c > d < e or a < b > c < d. Equal neighbours break
turbulence. A single element is turbulent (length 1). Return the length of the longest
turbulent subarray (0 for an empty list).
Examples: [9, 4, 2, 10, 7, 8, 8, 1, 9] -> 5 ([4, 2, 10, 7, 8]), [4, 8, 12, 16] -> 2, [100] -> 1.
Hint: track two running lengths -- "ends with an up step" and "ends with a down step" -- and
update both from the previous pair's comparison in one pass. O(n), O(1) space.

Run: python3 longest_turbulent_subarray.py
"""


def max_turbulence_size(arr):
    if not arr:
        return 0
    best = up = down = 1  # longest turbulent run ending here with an up / down last step
    for i in range(1, len(arr)):
        if arr[i] > arr[i - 1]:
            up, down = down + 1, 1
        elif arr[i] < arr[i - 1]:
            up, down = 1, up + 1
        else:
            up = down = 1
        best = max(best, up, down)
    return best


def _run_tests():
    assert max_turbulence_size([]) == 0
    assert max_turbulence_size([100]) == 1
    assert max_turbulence_size([9, 4, 2, 10, 7, 8, 8, 1, 9]) == 5
    assert max_turbulence_size([4, 8, 12, 16]) == 2
    assert max_turbulence_size([9, 9]) == 1
    assert max_turbulence_size([1, 2, 1, 2, 1]) == 5
    assert max_turbulence_size([0, 1, 1, 0, 1, 0, 1, 1, 0, 0]) == 5
    assert max_turbulence_size([5, 5, 5, 5]) == 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
