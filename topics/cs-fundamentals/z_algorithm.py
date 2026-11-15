"""
Day 55, Task 7 -- CS fundamentals: the Z-algorithm (Z-array + linear-time pattern search).

THE PROBLEM
------------
Part A -- z_array(s): return a list z of len(s) where z[i] is the length of the longest
substring starting at i that is also a PREFIX of s. By convention z[0] = len(s)
(and z_array("") == []).

  z_array("aabcaabxaaaz") -> [12, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0]
  z_array("aaaaa")        -> [5, 4, 3, 2, 1]

Part B -- find_all(text, pattern): return the sorted list of every start index where
pattern occurs in text (overlapping matches included), using the Z-array of
pattern + SEP + text where SEP is a character that occurs in neither string (or work with
lists and a unique sentinel object so ANY characters are allowed).
  find_all("abababa", "aba") -> [0, 2, 4]
  An empty pattern raises ValueError.

Part C -- smallest_period(s): the length p of the shortest string t such that s is a
prefix of t repeated enough times (i.e. s[i] == s[i - p] for all i >= p). Use the Z-array:
p is the smallest i >= 1 with i + z[i] == len(s), or len(s) if there is none.
  smallest_period("abcabcab") -> 3,  smallest_period("abcd") -> 4,  smallest_period("") -> 0

Hint for Part A: maintain the rightmost "Z-box" [l, r) that matches a prefix. For i < r,
start from min(r - i, z[i - l]) instead of 0, then extend by direct comparison; if the
match goes past r, move the box. Each character extends r at most once -> O(n).
A naive O(n^2) solution will time out on the 200k-character tests.

Run: python3 z_algorithm.py
"""


def z_array(s):
    n = len(s)
    if n == 0:
        return []
    z = [0] * n
    z[0] = n
    l = r = 0                         # rightmost Z-box [l, r) matching a prefix
    for i in range(1, n):
        k = min(r - i, z[i - l]) if i < r else 0
        while i + k < n and s[k] == s[i + k]:
            k += 1
        z[i] = k
        if i + k > r:
            l, r = i, i + k
    return z


_SENTINEL = object()                  # equal to no character, so any input is allowed


def find_all(text, pattern):
    if len(pattern) == 0:
        raise ValueError("pattern must be non-empty")
    m = len(pattern)
    combined = list(pattern) + [_SENTINEL] + list(text)
    z = z_array(combined)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] >= m]


def smallest_period(s):
    n = len(s)
    z = z_array(s)
    for i in range(1, n):
        if i + z[i] == n:
            return i
    return n


def _naive_z(s):
    n = len(s)
    out = []
    for i in range(n):
        k = 0
        while i + k < n and s[k] == s[i + k]:
            k += 1
        out.append(k)
    return out


def _run_tests():
    assert z_array("") == []
    assert z_array("a") == [1]
    assert z_array("aabcaabxaaaz") == [12, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0]
    assert z_array("aaaaa") == [5, 4, 3, 2, 1]
    assert z_array("abacaba") == [7, 0, 1, 0, 3, 0, 1]

    assert find_all("abababa", "aba") == [0, 2, 4]
    assert find_all("aaaa", "aa") == [0, 1, 2]
    assert find_all("hello", "xyz") == []
    assert find_all("abc", "abcd") == []
    assert find_all("needle in a haystack with needle", "needle") == [0, 26]
    assert find_all("a#b#a#b", "#b") == [1, 5]        # separator chars inside the input
    assert find_all("x$y$x", "$") == [1, 3]
    try:
        find_all("abc", "")
    except ValueError:
        pass
    else:
        raise AssertionError("empty pattern must raise ValueError")

    assert smallest_period("") == 0
    assert smallest_period("abcabcab") == 3
    assert smallest_period("abcd") == 4
    assert smallest_period("aaaa") == 1
    assert smallest_period("abaab") == 3

    import random
    rng = random.Random(55)
    for _ in range(400):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 30)))
        assert z_array(s) == _naive_z(s), s
        p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
        expected = [i for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p]
        assert find_all(s, p) == expected, (s, p)

    # Linear time on the worst case for naive matching.
    big = "a" * 200_000
    z = z_array(big)
    assert z[1] == 199_999 and z[-1] == 1
    assert len(find_all(big, "a" * 1000)) == 199_001
    assert smallest_period("ab" * 100_000) == 2

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
