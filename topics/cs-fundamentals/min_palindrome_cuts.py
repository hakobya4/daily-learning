"""
Day 46, Task 10 -- CS fundamentals: minimum cuts for palindrome partitioning (DP).

THE PROBLEM
------------
min_cuts(s) returns the minimum number of cuts needed to split s into pieces
that are all palindromes. "" and single characters need 0 cuts.
Hint: precompute is_pal[i][j] (or expand around centers), then
cuts[j] = 0 if s[:j+1] is a palindrome else min(cuts[i-1] + 1) over palindromic s[i..j]. O(n^2).

Run: python3 min_palindrome_cuts.py
"""


def min_cuts(s):
    raise NotImplementedError


def _run_tests():
    assert min_cuts("") == 0
    assert min_cuts("a") == 0
    assert min_cuts("aab") == 1
    assert min_cuts("aba") == 0
    assert min_cuts("ab") == 1
    assert min_cuts("abcde") == 4
    assert min_cuts("abccbc") == 2
    assert min_cuts("aaaa") == 0
    assert min_cuts("noonabbad") == 2
    assert min_cuts("a" * 200 + "b") == 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
