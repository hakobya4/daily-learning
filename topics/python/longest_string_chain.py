"""
Day 53, Task 2 -- Python: longest string chain (sort by length + hash-map DP).

THE PROBLEM
------------
longest_str_chain(words): word A is a PREDECESSOR of word B if you can insert exactly one
letter anywhere in A (without reordering the others) to get B -- e.g. "abc" -> "abac".
A word chain is a sequence w1, w2, ..., wk where each word is a predecessor of the next.
Return the length of the longest chain you can build from words (0 for an empty list; any
single word is a chain of length 1).
Examples: ["a", "b", "ba", "bca", "bda", "bdca"] -> 4 (a -> ba -> bda -> bdca),
          ["abcd", "dbqca"] -> 1.
Hint: sort words by length; best[w] = 1 + max(best[w with one char deleted]) over every
deletion that is a known word. O(n * L^2).

Run: python3 longest_string_chain.py
"""


def longest_str_chain(words):
    raise NotImplementedError


def _run_tests():
    assert longest_str_chain([]) == 0
    assert longest_str_chain(["a"]) == 1
    assert longest_str_chain(["a", "b", "ba", "bca", "bda", "bdca"]) == 4
    assert longest_str_chain(["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"]) == 5
    assert longest_str_chain(["abcd", "dbqca"]) == 1
    assert longest_str_chain(["a", "ab", "ac", "abc", "abcd", "bd"]) == 4
    assert longest_str_chain(["ab", "abc", "ab"]) == 2
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
