"""
Day 37, Task 2 -- Python: longest substring with at most K distinct characters.

THE PROBLEM
------------
Given a string s and an integer k, return the length of the longest
substring that contains at most k distinct characters. k == 0 -> 0.

  ("eceba", 2)   -> 3   ("ece")
  ("aa", 1)      -> 2
  ("abc", 0)     -> 0
  ("", 3)        -> 0

HOW TO WORK THROUGH THIS
-------------------------
Sliding window with a character -> count dict. Grow the right edge; while
the dict has more than k keys, shrink from the left (delete keys whose
count hits 0). Track the best window length. O(n).

Run: python3 longest_subarray_k_distinct.py
"""


def longest_k_distinct(s: str, k: int) -> int:
    if k <= 0:
        return 0
    counts = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) > k:
            lc = s[left]
            counts[lc] -= 1
            if counts[lc] == 0:
                del counts[lc]
            left += 1
        best = max(best, right - left + 1)
    return best


def _run_tests():
    assert longest_k_distinct("eceba", 2) == 3
    assert longest_k_distinct("aa", 1) == 2
    assert longest_k_distinct("abc", 0) == 0
    assert longest_k_distinct("", 3) == 0
    assert longest_k_distinct("abcabc", 3) == 6
    assert longest_k_distinct("abaccc", 2) == 4
    assert longest_k_distinct("a", 5) == 1
    assert longest_k_distinct("aabbcc", 1) == 2
    assert longest_k_distinct("abcdef", 2) == 2
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
