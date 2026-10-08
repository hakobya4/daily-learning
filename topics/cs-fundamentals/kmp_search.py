"""
Day 17, Task 10 -- CS fundamentals: KMP substring search.

THE PROBLEM
------------
Implement Knuth-Morris-Pratt without using str.find / str.index / re.

  build_lps(p)        -> list; lps[i] = length of the longest proper prefix
                         of p[:i+1] that is also a suffix of it.
                         build_lps("aabaaab") -> [0, 1, 0, 1, 2, 2, 3]
  kmp_find_all(t, p)  -> sorted list of every start index where p occurs in
                         t, INCLUDING overlapping matches.
                         kmp_find_all("aaaa", "aa") -> [0, 1, 2]
                         kmp_find_all("abcabc", "bc") -> [1, 4]
  An empty pattern raises ValueError.

HOW TO WORK THROUGH THIS
-------------------------
On a mismatch after k matched chars, fall back to k = lps[k-1] instead of
restarting -- the text pointer never moves backwards, so it is O(n + m).

Run: python3 kmp_search.py
"""


def build_lps(p: str) -> list:
    lps = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k > 0 and p[i] != p[k]:
            k = lps[k - 1]
        if p[i] == p[k]:
            k += 1
        lps[i] = k
    return lps


def kmp_find_all(t: str, p: str) -> list:
    if not p:
        raise ValueError("empty pattern")
    lps = build_lps(p)
    res = []
    k = 0
    for i, ch in enumerate(t):
        while k > 0 and ch != p[k]:
            k = lps[k - 1]
        if ch == p[k]:
            k += 1
        if k == len(p):
            res.append(i - k + 1)
            k = lps[k - 1]
    return res


def _run_tests():
    assert build_lps("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
    assert build_lps("abcd") == [0, 0, 0, 0]
    assert build_lps("aaaa") == [0, 1, 2, 3]
    assert build_lps("a") == [0]
    assert kmp_find_all("aaaa", "aa") == [0, 1, 2]
    assert kmp_find_all("abcabc", "bc") == [1, 4]
    assert kmp_find_all("abc", "abcd") == []
    assert kmp_find_all("", "a") == []
    assert kmp_find_all("ababcabababd", "ababd") == [7]
    assert kmp_find_all("abababab", "abab") == [0, 2, 4]
    try:
        kmp_find_all("abc", "")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
