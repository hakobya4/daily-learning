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
    from collections import Counter
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best = (0, 0)
    best_len = float("inf")
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best = (left, right + 1)
            need[s[left]] += 1
            missing += 1
            left += 1
    return s[best[0]:best[1]] if best_len != float("inf") else ""


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
