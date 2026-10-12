"""
Day 21, Task 10 -- CS fundamentals: Rabin-Karp substring search.

THE PROBLEM
------------
Implement find_all(text, pattern) returning every start index (including
overlapping matches) where pattern occurs in text, using a ROLLING hash
so each window hash is updated in O(1).

  find_all("abababa", "aba") == [0, 2, 4]
  find_all("aaaa", "aa")     == [0, 1, 2]
  find_all("hello", "xyz")   == []

Raise ValueError for an empty pattern. A hash match must be confirmed by
comparing the actual substring (hashes can collide).

HOW TO WORK THROUGH THIS
-------------------------
h = sum(ord(c) * B**(m-1-i)) mod M. To slide: remove the leading char's
contribution (ord * B**(m-1)), multiply by B, add the new char. Use a
small modulus in your own experiments to see collisions happen.

Run: python3 rabin_karp.py
"""


def find_all(text: str, pattern: str) -> list:
    if not pattern:
        raise ValueError("empty pattern")
    n, m = len(text), len(pattern)
    if m > n:
        return []
    B, M = 256, 1_000_000_007
    high = pow(B, m - 1, M)
    hp = ht = 0
    for i in range(m):
        hp = (hp * B + ord(pattern[i])) % M
        ht = (ht * B + ord(text[i])) % M
    res = []
    for i in range(n - m + 1):
        if hp == ht and text[i:i + m] == pattern:
            res.append(i)
        if i + m < n:
            ht = ((ht - ord(text[i]) * high) * B + ord(text[i + m])) % M
    return res


def _run_tests():
    import random

    assert find_all("abababa", "aba") == [0, 2, 4]
    assert find_all("aaaa", "aa") == [0, 1, 2]
    assert find_all("hello", "xyz") == []
    assert find_all("abc", "abcd") == []
    assert find_all("abc", "abc") == [0]
    assert find_all("", "a") == []
    try:
        find_all("abc", "")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    rnd = random.Random(3)
    for _ in range(200):
        text = "".join(rnd.choice("ab") for _ in range(rnd.randint(0, 40)))
        pat = "".join(rnd.choice("ab") for _ in range(rnd.randint(1, 5)))
        naive = [i for i in range(len(text) - len(pat) + 1)
                 if text[i:i + len(pat)] == pat]
        assert find_all(text, pat) == naive, (text, pat)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
