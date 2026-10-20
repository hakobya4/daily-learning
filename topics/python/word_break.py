"""
Day 30, Task 4 -- Python: word break (DP over prefixes).

THE PROBLEM
------------
word_break(s, words) -> True if s can be split into a sequence of one or
more words from the list (words may be reused, order of the list is
irrelevant). The empty string is breakable.

  "leetcode",  ["leet","code"]            -> True
  "applepenapple", ["apple","pen"]        -> True
  "catsandog", ["cats","dog","sand","and","cat"] -> False

HOW TO WORK THROUGH THIS
-------------------------
dp[i] = True if s[:i] is breakable; dp[0] = True; dp[i] is True if some j<i
has dp[j] and s[j:i] in the word set. Put the words in a set first.

Run: python3 word_break.py
"""


def word_break(s: str, words: list) -> bool:
    raise NotImplementedError


def _run_tests():
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    assert word_break("", ["a"]) is True
    assert word_break("a", []) is False
    assert word_break("aaaaaaa", ["aaaa", "aaa"]) is True
    assert word_break("aaaaaaab", ["a", "aa"]) is False
    assert word_break("abcd", ["a", "abc", "b", "cd"]) is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
