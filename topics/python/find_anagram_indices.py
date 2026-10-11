"""
Day 20, Task 4 -- Python: find all anagram start indices.

THE PROBLEM
------------
Return the start indices (ascending) of every substring of s that is an
anagram of p.

  find_anagrams("cbaebabacd", "abc") -> [0, 6]
  find_anagrams("abab", "ab")        -> [0, 1, 2]
  find_anagrams("a", "ab")           -> []

Raise ValueError if p is empty.

HOW TO WORK THROUGH THIS
-------------------------
Fixed-size sliding window of len(p) with a letter-count comparison; update
the counts incrementally instead of rebuilding them. O(len(s)).

Run: python3 find_anagram_indices.py
"""


def find_anagrams(s: str, p: str) -> list:
    if not p:
        raise ValueError("p must not be empty")
    n, m = len(s), len(p)
    if n < m:
        return []
    need = {}
    for ch in p:
        need[ch] = need.get(ch, 0) + 1
    window = {}
    result = []
    for i, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if i >= m:
            old = s[i - m]
            window[old] -= 1
            if window[old] == 0:
                del window[old]
        if i >= m - 1 and window == need:
            result.append(i - m + 1)
    return result


def _run_tests():
    assert find_anagrams("cbaebabacd", "abc") == [0, 6]
    assert find_anagrams("abab", "ab") == [0, 1, 2]
    assert find_anagrams("a", "ab") == []
    assert find_anagrams("", "a") == []
    assert find_anagrams("aaaa", "aa") == [0, 1, 2]
    assert find_anagrams("abc", "abc") == [0]
    assert find_anagrams("abc", "abd") == []
    try:
        find_anagrams("abc", "")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
