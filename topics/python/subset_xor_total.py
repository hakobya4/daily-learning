"""
Day 51, Task 1 -- Python: sum of all subset XOR totals.

THE PROBLEM
------------
subset_xor_total(nums): the XOR total of a subset is the XOR of all its elements
(the empty subset has total 0). Return the SUM of the XOR totals of every subset of nums.
Examples: [1, 3] -> 6 (subsets: {}=0, {1}=1, {3}=3, {1,3}=2), [5, 1, 6] -> 28.
Hint: brute force with bitmasks works for n <= 12; there is also an O(n) trick with OR
(every set bit of the OR appears in exactly half of the 2**n subsets).

Run: python3 subset_xor_total.py
"""


def subset_xor_total(nums):
    # Every bit set in the OR of all numbers is set in exactly half of the 2**n subsets'
    # XOR totals, so the sum is OR * 2**(n-1). Empty input -> 0.
    if not nums:
        return 0
    acc = 0
    for x in nums:
        acc |= x
    return acc << (len(nums) - 1)


def _run_tests():
    assert subset_xor_total([]) == 0
    assert subset_xor_total([1, 3]) == 6
    assert subset_xor_total([5, 1, 6]) == 28
    assert subset_xor_total([3, 4, 5, 6, 7, 8]) == 480
    assert subset_xor_total([7]) == 7
    assert subset_xor_total([2, 2]) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
