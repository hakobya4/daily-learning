"""
Day 35, Task 4 -- Python: permutation in string (sliding window).

THE PROBLEM
------------
Return True if s2 contains a permutation of s1 as a CONTIGUOUS substring
(i.e. some window of s2 of length len(s1) has exactly the same letter
counts as s1). Lowercase letters only.

  s1="ab",  s2="eidbaooo" -> True   ("ba")
  s1="ab",  s2="eidboaoo" -> False
  s1="",    s2="abc"      -> True   (empty permutation always fits)

HOW TO WORK THROUGH THIS
-------------------------
Keep two count arrays of size 26 (or Counters): one for s1, one for the
current window of s2. Slide the window one char at a time (add the new
right char, drop the old left char) and compare the counts in O(26).

Run: python3 permutation_in_string.py
"""


def check_inclusion(s1: str, s2: str) -> bool:
    raise NotImplementedError


def _run_tests():
    assert check_inclusion("ab", "eidbaooo") is True
    assert check_inclusion("ab", "eidboaoo") is False
    assert check_inclusion("", "abc") is True
    assert check_inclusion("abc", "ab") is False
    assert check_inclusion("adc", "dcda") is True
    assert check_inclusion("hello", "ooolleoooleh") is False
    assert check_inclusion("a", "a") is True
    assert check_inclusion("aab", "cbaabc") is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
