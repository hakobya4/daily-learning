"""
Day 30, Task 2 -- Python: rotate an array in place.

THE PROBLEM
------------
rotate(nums, k) rotates the list to the RIGHT by k steps, in place, and
returns None. k may be 0, larger than len(nums), or the list may be empty.

  [1,2,3,4,5,6,7], k=3 -> [5,6,7,1,2,3,4]
  [-1,-100,3,99], k=2  -> [3,99,-1,-100]

HOW TO WORK THROUGH THIS
-------------------------
Easy: nums[:] = nums[-k:] + nums[:-k] (after k %= n).
Stretch goal: O(1) extra space with three reversals (all, first k, rest).

Run: python3 rotate_array.py
"""


def rotate(nums: list, k: int) -> None:
    n = len(nums)
    if n == 0:
        return
    k %= n

    def rev(i, j):
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1

    rev(0, n - 1)
    rev(0, k - 1)
    rev(k, n - 1)


def _run_tests():
    a = [1, 2, 3, 4, 5, 6, 7]
    assert rotate(a, 3) is None
    assert a == [5, 6, 7, 1, 2, 3, 4]
    a = [-1, -100, 3, 99]
    rotate(a, 2)
    assert a == [3, 99, -1, -100]
    a = [1, 2, 3]
    rotate(a, 0)
    assert a == [1, 2, 3]
    a = [1, 2, 3]
    rotate(a, 3)
    assert a == [1, 2, 3]
    a = [1, 2, 3]
    rotate(a, 4)
    assert a == [3, 1, 2]
    a = []
    rotate(a, 5)
    assert a == []
    a = [9]
    rotate(a, 100)
    assert a == [9]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
