"""
Day 17, Task 3 -- Python: longest substring without repeating characters.

THE PROBLEM
------------
Return the length of the longest substring of s with all distinct chars,
and (second function) the first such substring of maximal length.

    length_of_longest_unique("abcabcbb") -> 3     # "abc"
    length_of_longest_unique("bbbbb")    -> 1
    length_of_longest_unique("pwwkew")   -> 3     # "wke"
    length_of_longest_unique("")         -> 0
    longest_unique("pwwkew")             -> "wke"
    longest_unique("abba")               -> "ab"  # first of max length

HOW TO WORK THROUGH THIS
-------------------------
Sliding window with a dict of last-seen index; when you see a repeat,
move the left edge to max(left, last_seen[ch] + 1). O(n).

Run: python3 longest_unique_substring.py
"""


def length_of_longest_unique(s: str) -> int:
    raise NotImplementedError


def longest_unique(s: str) -> str:
    raise NotImplementedError


def _run_tests():
    assert length_of_longest_unique("abcabcbb") == 3
    assert length_of_longest_unique("bbbbb") == 1
    assert length_of_longest_unique("pwwkew") == 3
    assert length_of_longest_unique("") == 0
    assert length_of_longest_unique("abba") == 2
    assert length_of_longest_unique("tmmzuxt") == 5
    assert longest_unique("pwwkew") == "wke"
    assert longest_unique("abba") == "ab"
    assert longest_unique("") == ""
    assert longest_unique("dvdf") == "vdf"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
