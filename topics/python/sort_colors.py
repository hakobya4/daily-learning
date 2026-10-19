"""
Day 28, Task 4 -- Python: sort colors (Dutch national flag).

THE PROBLEM
------------
sort_colors(nums) sorts a list containing only 0, 1 and 2 IN PLACE, in a
single pass, without using sort()/sorted() and without counting then
rewriting. It returns None.

  nums = [2, 0, 2, 1, 1, 0]  ->  [0, 0, 1, 1, 2, 2]

HOW TO WORK THROUGH THIS
-------------------------
Three pointers: low (next slot for 0), high (next slot for 2) and i
(scanner). Swap 0s to the front, 2s to the back, leave 1s. Careful: after
swapping with high, do not advance i.

Run: python3 sort_colors.py
"""


def sort_colors(nums: list) -> None:
    low, i, high = 0, 0, len(nums) - 1
    while i <= high:
        if nums[i] == 0:
            nums[low], nums[i] = nums[i], nums[low]
            low += 1
            i += 1
        elif nums[i] == 2:
            nums[high], nums[i] = nums[i], nums[high]
            high -= 1
        else:
            i += 1


def _run_tests():
    cases = [
        [2, 0, 2, 1, 1, 0],
        [2, 0, 1],
        [0],
        [],
        [1, 1, 1],
        [2, 2, 1, 1, 0, 0],
        [0, 1, 2, 0, 1, 2, 0, 1, 2],
    ]
    for case in cases:
        nums = list(case)
        result = sort_colors(nums)
        assert result is None, "must sort in place and return None"
        assert nums == sorted(case), (case, nums)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
