"""
Day 23, Task 3 -- Python: word pattern (bijection).

THE PROBLEM
------------
Given a pattern string of letters and a string s of space-separated words,
return True iff s follows the pattern: there is a ONE-TO-ONE mapping
(bijection) between pattern letters and words.

  word_pattern("abba", "dog cat cat dog")   is True
  word_pattern("abba", "dog cat cat fish")  is False
  word_pattern("aaaa", "dog cat cat dog")   is False
  word_pattern("abba", "dog dog dog dog")   is False  (two letters, one word)

The lengths must match too: word_pattern("a", "") is False,
word_pattern("", "") is True.

HOW TO WORK THROUGH THIS
-------------------------
Keep two dicts (letter -> word and word -> letter) and check both
directions while walking pattern and s.split() together.

Run: python3 word_pattern.py
"""


def word_pattern(pattern: str, s: str) -> bool:
    raise NotImplementedError


def _run_tests():
    assert word_pattern("abba", "dog cat cat dog") is True
    assert word_pattern("abba", "dog cat cat fish") is False
    assert word_pattern("aaaa", "dog cat cat dog") is False
    assert word_pattern("abba", "dog dog dog dog") is False
    assert word_pattern("a", "") is False
    assert word_pattern("", "") is True
    assert word_pattern("ab", "dog") is False
    assert word_pattern("abc", "b c a") is True
    assert word_pattern("aba", "x y x") is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
