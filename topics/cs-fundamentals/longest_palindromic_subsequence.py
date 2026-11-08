"""
Day 49, Task 9 -- CS fundamentals: longest palindromic subsequence (DP).

THE PROBLEM
------------
lps(s) returns the LENGTH of the longest subsequence of s (characters in order, not
necessarily contiguous) that reads the same forwards and backwards.
Examples: 'bbbab' -> 4 ('bbbb'), 'cbbd' -> 2 ('bb'), 'a' -> 1, '' -> 0.
Hint: dp[i][j] for s[i..j]; if s[i]==s[j] then 2 + dp[i+1][j-1] else max(dp[i+1][j], dp[i][j-1]).
(Alternative: LCS of s and its reverse.) Aim for O(n^2) time.

Run: python3 longest_palindromic_subsequence.py
"""


def lps(s):
    raise NotImplementedError


def _run_tests():
    assert lps("bbbab") == 4
    assert lps("cbbd") == 2
    assert lps("a") == 1
    assert lps("") == 0
    assert lps("abcde") == 1
    assert lps("racecar") == 7
    assert lps("character") == 5
    assert lps("agbdba") == 5
    assert lps("x" * 200) == 200
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
