"""
Day 33, Task 4 -- Python: find the duplicate number (no modification).

THE PROBLEM
------------
nums has n + 1 integers, each in the range 1..n inclusive, so at least one
value repeats. Exactly one value is the "duplicate" (it may appear more
than twice). Return it WITHOUT modifying nums and using O(1) extra space.

  [1, 3, 4, 2, 2]  -> 2
  [3, 1, 3, 4, 2]  -> 3
  [1, 1]           -> 1
  [2, 2, 2, 2, 2]  -> 2

HOW TO WORK THROUGH THIS
-------------------------
Treat the list as a linked list where index i points to nums[i]. A
duplicate means two indices point to the same node, so the list has a
cycle and the duplicate is the cycle's entrance. Use Floyd's tortoise and
hare: find a meeting point, then restart one pointer from 0 and advance
both one step at a time until they meet.

Run: python3 find_duplicate_number.py
"""


def find_duplicate(nums: list) -> int:
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


def _run_tests():
    assert find_duplicate([1, 3, 4, 2, 2]) == 2
    assert find_duplicate([3, 1, 3, 4, 2]) == 3
    assert find_duplicate([1, 1]) == 1
    assert find_duplicate([2, 2, 2, 2, 2]) == 2
    assert find_duplicate([1, 4, 4, 2, 4]) == 4
    nums = [5, 3, 1, 2, 4, 6, 5]
    snapshot = list(nums)
    assert find_duplicate(nums) == 5
    assert nums == snapshot, "input must not be modified"
    big = list(range(1, 1001)) + [777]
    assert find_duplicate(big) == 777
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
