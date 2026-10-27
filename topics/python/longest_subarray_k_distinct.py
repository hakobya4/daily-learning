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
    raise NotImplementedError


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
