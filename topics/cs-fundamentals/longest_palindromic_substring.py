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


def longest_palindrome(s: str) -> str:
    raise NotImplementedError


def count_palindromic_substrings(s: str) -> int:
    raise NotImplementedError


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
