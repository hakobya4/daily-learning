"""
Day 45, Task 2 -- Python: majority element II (Boyer-Moore voting).

THE PROBLEM
------------
majority_elements(nums) returns, as a sorted list, every value that appears
MORE than len(nums)//3 times. Use O(n) time and O(1) extra space (at most two
candidates).
Hint: generalized Boyer-Moore with two candidates + counts, then a second pass
to verify the candidates.

Run: python3 majority_element_ii.py
"""


def majority_elements(nums):
    c1 = c2 = None
    n1 = n2 = 0
    for x in nums:
        if x == c1:
            n1 += 1
        elif x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:
            n1 -= 1
            n2 -= 1
    limit = len(nums) // 3
    result = []
    for c in (c1, c2):
        if c is not None and c not in result and nums.count(c) > limit:
            result.append(c)
    return sorted(result)


def _run_tests():
    assert majority_elements([3, 2, 3]) == [3]
    assert majority_elements([1]) == [1]
    assert majority_elements([1, 2]) == [1, 2]
    assert majority_elements([1, 1, 1, 3, 3, 2, 2, 2]) == [1, 2]
    assert majority_elements([]) == []
    assert majority_elements([1, 2, 3, 4]) == []
    assert majority_elements([2, 2, 1, 1, 1, 2, 2]) == [1, 2]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
