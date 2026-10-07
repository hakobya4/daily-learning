"""
Day 17, Task 4 -- Python: minimum window substring.

THE PROBLEM
------------
Given strings s and t, return the shortest substring of s that contains
every character of t (with multiplicity). If several windows tie, return
the leftmost. If none exists, return "". An empty t returns "".

    min_window("ADOBECODEBANC", "ABC") -> "BANC"
    min_window("a", "a")               -> "a"
    min_window("a", "aa")              -> ""
    min_window("aab", "ab")            -> "ab"

HOW TO WORK THROUGH THIS
-------------------------
Two pointers + a Counter of what is still needed. Expand right until the
window is valid, then shrink from the left while it stays valid.

Run: python3 min_window_substring.py
"""


def min_window(s: str, t: str) -> str:
    raise NotImplementedError


def _run_tests():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
    assert min_window("aab", "ab") == "ab"
    assert min_window("abc", "") == ""
    assert min_window("", "a") == ""
    assert min_window("abcabdebac", "cda") == "cabd"
    assert min_window("aaflslflsldkalskaaa", "aaa") == "aaa"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
