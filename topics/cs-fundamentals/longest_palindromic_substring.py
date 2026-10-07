"""
Day 16, Task 10 -- CS fundamentals: longest palindromic substring.

THE PROBLEM
------------
longest_palindrome(s) returns the longest substring of s that reads the
same forwards and backwards. On ties return the one that starts
EARLIEST. Empty string -> "".

    longest_palindrome("babad")   -> "bab"
    longest_palindrome("cbbd")    -> "bb"
    longest_palindrome("a")       -> "a"
    longest_palindrome("forgeeksskeegfor") -> "geeksskeeg"

Also implement count_palindromic_substrings(s): the number of
(start, end) index pairs whose substring is a palindrome.

    count_palindromic_substrings("abc") -> 3
    count_palindromic_substrings("aaa") -> 6

HOW TO WORK THROUGH THIS
-------------------------
Expand around each of the 2n-1 centers: O(n^2) time, O(1) space.
(Manacher's algorithm gets O(n) if you want a stretch goal.)

Run: python3 longest_palindromic_substring.py
"""


def _expand(s: str, lo: int, hi: int):
    while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
        lo -= 1
        hi += 1
    return lo + 1, hi  # [start, end)


def longest_palindrome(s: str) -> str:
    best_start, best_end = 0, 0
    for center in range(2 * len(s) - 1):
        lo = center // 2
        hi = lo + center % 2
        a, b = _expand(s, lo, hi)
        if b - a > best_end - best_start:
            best_start, best_end = a, b
    return s[best_start:best_end]


def count_palindromic_substrings(s: str) -> int:
    total = 0
    for center in range(2 * len(s) - 1):
        lo = center // 2
        hi = lo + center % 2
        a, b = _expand(s, lo, hi)
        total += (b - a + 1) // 2
    return total


def _run_tests():
    assert longest_palindrome("babad") == "bab"
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("a") == "a"
    assert longest_palindrome("") == ""
    assert longest_palindrome("abc") == "a"
    assert longest_palindrome("forgeeksskeegfor") == "geeksskeeg"
    assert longest_palindrome("x" * 50) == "x" * 50
    assert count_palindromic_substrings("abc") == 3
    assert count_palindromic_substrings("aaa") == 6
    assert count_palindromic_substrings("") == 0
    assert count_palindromic_substrings("abba") == 6
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
