"""
Day 49, Task 3 -- Python: in-place string compression of a list of characters.

THE PROBLEM
------------
compress(chars) takes a list of single-character strings and compresses it IN PLACE
using run-length encoding: each run of a character c of length n becomes c followed by
the digits of n, but the count is omitted when n == 1 (so 'a','a','a' -> 'a','3'; a
lone 'b' stays 'b'). Counts of 10 or more are split into separate characters ('1','2').
The function returns the new length, and chars[:new_length] must hold the result.
Use O(1) extra space (no building a second list of the answer).
Examples: list('aabbccc') -> 6 with chars[:6] == list('a2b2c3');
list('a'*12) -> 3 ('a','1','2').
Hint: two pointers -- a read pointer finding run ends, a write pointer.

Run: python3 string_compression_inplace.py
"""


def compress(chars):
    raise NotImplementedError


def _run_tests():
    c = list("aabbccc")
    n = compress(c)
    assert n == 6 and c[:n] == list("a2b2c3")
    c = list("a")
    n = compress(c)
    assert n == 1 and c[:n] == ["a"]
    c = list("a" * 12)
    n = compress(c)
    assert n == 3 and c[:n] == ["a", "1", "2"]
    c = list("abbbbbbbbbbbb")
    n = compress(c)
    assert n == 4 and c[:n] == ["a", "b", "1", "2"]
    c = []
    assert compress(c) == 0
    c = list("abc")
    n = compress(c)
    assert n == 3 and c[:n] == list("abc")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
