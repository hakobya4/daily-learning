"""
Day 15, Task 2 -- Python: next lexicographic permutation.

THE PROBLEM
------------
next_permutation(nums) rearranges the list IN PLACE into the next
lexicographically greater permutation and returns True. If the list is
already the greatest (descending), rearrange it into the smallest
(ascending) and return False.

    [1, 2, 3] -> [1, 3, 2]  True
    [1, 3, 2] -> [2, 1, 3]  True
    [3, 2, 1] -> [1, 2, 3]  False
    [1, 1, 5] -> [1, 5, 1]  True

Must be O(n) time, O(1) extra space, and handle duplicates and [] / [x].

HOW TO WORK THROUGH THIS
-------------------------
Find the rightmost i with nums[i] < nums[i+1]; swap nums[i] with the
rightmost element greater than it; reverse the suffix after i.

Run: python3 next_permutation.py
"""


def next_permutation(nums: list[int]) -> bool:
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    found = i >= 0
    if found:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    lo, hi = i + 1, n - 1
    while lo < hi:
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo += 1
        hi -= 1
    return found


def _run_tests() -> None:
    a = [1, 2, 3]
    assert next_permutation(a) is True and a == [1, 3, 2]
    a = [1, 3, 2]
    assert next_permutation(a) is True and a == [2, 1, 3]
    a = [3, 2, 1]
    assert next_permutation(a) is False and a == [1, 2, 3]
    a = [1, 1, 5]
    assert next_permutation(a) is True and a == [1, 5, 1]
    a = [2, 2, 2]
    assert next_permutation(a) is False and a == [2, 2, 2]
    a = []
    assert next_permutation(a) is False and a == []
    a = [7]
    assert next_permutation(a) is False and a == [7]
    # walk all permutations of 4 distinct items: 24 of them, then wrap
    a = [1, 2, 3, 4]
    seen = [tuple(a)]
    while next_permutation(a):
        seen.append(tuple(a))
    assert len(seen) == 24 and seen == sorted(seen) and a == [1, 2, 3, 4]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
