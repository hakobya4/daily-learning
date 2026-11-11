"""
Day 52, Task 2 -- Python: count binary substrings (run-length groups).

THE PROBLEM
------------
count_binary_substrings(s): s consists only of '0' and '1'. Count the non-empty substrings
that have the same number of 0s and 1s AND where all the 0s are grouped together and all the
1s are grouped together (e.g. "0011" and "10" count, "0101" does not). Substrings that occur
several times are counted once per occurrence.
Examples: "00110011" -> 6 ("0011", "01", "1100", "10", "0011", "01"), "10101" -> 4.
Hint: compress s into run lengths (e.g. "0011100" -> [2, 3, 2]); each pair of neighbouring
runs (a, b) contributes min(a, b). O(n) time, O(1) extra space is possible.

Run: python3 count_binary_substrings.py
"""


def count_binary_substrings(s):
    raise NotImplementedError


def _run_tests():
    assert count_binary_substrings("") == 0
    assert count_binary_substrings("0") == 0
    assert count_binary_substrings("00110011") == 6
    assert count_binary_substrings("10101") == 4
    assert count_binary_substrings("000111") == 3
    assert count_binary_substrings("0011100") == 4
    assert count_binary_substrings("1111") == 0
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
