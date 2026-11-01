"""
Day 41, Task 3 -- Python: find all anagram start indices.

THE PROBLEM
------------
find_anagrams(s, p) returns the sorted list of start indices i such that
s[i:i+len(p)] is an anagram of p (same letters, same counts). Lowercase
letters only. O(len(s)) with a sliding window of counts. If p is empty or
longer than s, return [].

  find_anagrams("cbaebabacd", "abc") -> [0, 6]
  find_anagrams("abab", "ab")        -> [0, 1, 2]

Also implement is_anagram(a, b) -> bool (case-sensitive, spaces count).

Run: python3 running_anagram_index.py
"""


def find_anagrams(s: str, p: str) -> list:
    raise NotImplementedError


def is_anagram(a: str, b: str) -> bool:
    raise NotImplementedError


def _run_tests():
    assert find_anagrams("cbaebabacd", "abc") == [0, 6]
    assert find_anagrams("abab", "ab") == [0, 1, 2]
    assert find_anagrams("a", "ab") == []
    assert find_anagrams("abc", "") == []
    assert find_anagrams("aaaaa", "aa") == [0, 1, 2, 3]
    assert find_anagrams("xyz", "abc") == []
    assert find_anagrams("ab" * 500, "ba") == list(range(999))
    assert is_anagram("listen", "silent") is True
    assert is_anagram("a b", "ab ") is True
    assert is_anagram("abc", "abd") is False
    assert is_anagram("Ab", "ab") is False
    assert is_anagram("", "") is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
