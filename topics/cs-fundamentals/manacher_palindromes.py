"""
Day 56, Task 4 -- CS fundamentals: Manacher's algorithm (all palindromes in O(n)).

THE PROBLEM
------------
Implement Manacher's algorithm and use it for three queries:

  * radii(s)               -- the list d over the TRANSFORMED string t = "#" + "#".join(s) + "#"
                              (length 2n+1), where d[i] is the largest r such that
                              t[i-r .. i+r] is a palindrome. (So for s = "aba",
                              t = "#a#b#a#" and d = [0, 1, 0, 3, 0, 1, 0].)
  * longest_palindrome(s)  -- the longest palindromic substring; on ties return the
                              LEFTMOST one. "" for "".
  * count_palindromes(s)   -- the number of palindromic substrings counted by position
                              ("aaa" has 6: a, a, a, aa, aa, aaa).

Rules:
  * Everything must run in O(n). The tests run on 200_000-character strings, where the
    O(n^2) expand-around-center approach is far too slow.
  * Do not actually need "#" to be absent from s -- the transform is conceptual; work on
    indices if you prefer, but radii() must return the list described above.

Hint: keep the rightmost palindrome found so far as (center c, right edge r). For a new
position i < r, its mirror is j = 2c - i and d[i] starts at min(d[j], r - i) -- that much
is guaranteed for free. Then try to expand naively past r and update (c, r) if you got
further right. Every naive comparison moves r right, so the total work is O(n).
In the transformed string, d[i] equals the length of the corresponding palindrome in s,
and its start in s is (i - d[i]) // 2. A center with radius d[i] contributes
(d[i] + 1) // 2 palindromes to the count.

Run: python3 manacher_palindromes.py
"""


def radii(s):
    raise NotImplementedError


def longest_palindrome(s):
    raise NotImplementedError


def count_palindromes(s):
    raise NotImplementedError


def _naive_longest(s):
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub = s[i:j + 1]
            if len(sub) > len(best) and sub == sub[::-1]:
                best = sub
    return best


def _naive_count(s):
    return sum(1 for i in range(len(s)) for j in range(i, len(s))
               if s[i:j + 1] == s[i:j + 1][::-1])


def _run_tests():
    assert radii("") == [0]
    assert radii("a") == [0, 1, 0]
    assert radii("aba") == [0, 1, 0, 3, 0, 1, 0]
    assert radii("aa") == [0, 1, 2, 1, 0]
    assert radii("abba") == [0, 1, 0, 1, 4, 1, 0, 1, 0]

    assert longest_palindrome("") == ""
    assert longest_palindrome("a") == "a"
    assert longest_palindrome("babad") == "bab"
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("forgeeksskeegfor") == "geeksskeeg"
    assert longest_palindrome("abcd") == "a"
    assert longest_palindrome("xabax#yzzy") == "xabax"

    assert count_palindromes("") == 0
    assert count_palindromes("abc") == 3
    assert count_palindromes("aaa") == 6
    assert count_palindromes("abba") == 6

    import random
    rng = random.Random(56)
    for _ in range(400):
        s = "".join(rng.choice("ab#") for _ in range(rng.randint(0, 25)))
        assert longest_palindrome(s) == _naive_longest(s), s
        assert count_palindromes(s) == _naive_count(s), s
        d = radii(s)
        assert len(d) == 2 * len(s) + 1

    n = 200_000
    assert count_palindromes("a" * n) == n * (n + 1) // 2
    assert len(longest_palindrome("ab" * (n // 2))) == n - 1
    s = "".join(rng.choice("ab") for _ in range(n))
    assert len(radii(s)) == 2 * n + 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
