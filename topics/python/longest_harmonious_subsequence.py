"""
Day 36, Task 3 -- Python: longest harmonious subsequence (hash counting).

THE PROBLEM
------------
A harmonious sequence is one whose max and min differ by EXACTLY 1.
Return the length of the longest harmonious subsequence of nums (order
does not matter for the length, so you may pick any elements). 0 if none.

  [1,3,2,2,5,2,3,7] -> 5   (3,2,2,2,3)
  [1,2,3,4]         -> 2
  [1,1,1,1]         -> 0

HOW TO WORK THROUGH THIS
-------------------------
Count each value. For every value v with v+1 also present, the candidate
is count[v] + count[v+1]. Take the best. O(n).

Run: python3 longest_harmonious_subsequence.py
"""


def find_lhs(nums: list[int]) -> int:
    from collections import Counter
    count = Counter(nums)
    best = 0
    for v, c in count.items():
        if v + 1 in count:
            best = max(best, c + count[v + 1])
    return best


def _run_tests():
    assert find_lhs([1, 3, 2, 2, 5, 2, 3, 7]) == 5
    assert find_lhs([1, 2, 3, 4]) == 2
    assert find_lhs([1, 1, 1, 1]) == 0
    assert find_lhs([]) == 0
    assert find_lhs([-1, 0, -1, 0, -1]) == 5
    assert find_lhs([1, 2, 2, 1]) == 4
    assert find_lhs([5]) == 0
    assert find_lhs([1, 4, 7, 10]) == 0
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
