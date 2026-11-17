"""
Day 58, Task 1 -- Python: minimum window SUBSEQUENCE (not substring) with DP / two pointers.

THE PROBLEM
------------
Given strings s and t, return the SHORTEST contiguous substring w of s such that t is a
SUBSEQUENCE of w (the characters of t appear in w in order, not necessarily adjacent).
  * If several shortest windows exist, return the LEFTMOST one.
  * If no window exists, or t is empty, return "".
Characters are compared exactly (case-sensitive).

Example:
  min_window_subsequence("abcdebdde", "bde")      -> "bcde"
      ("bcde" and "bdde" both have length 4; "bcde" starts first)
  min_window_subsequence("jmeqksfrsdcmsiwvaovztaqenprpvnbstl", "u") -> ""
  min_window_subsequence("aaaa", "aa")            -> "aa"
  min_window_subsequence("fgrqsqsnodwmxzkzxwqegkndaa", "kzed") -> "kzxwqegknd"

Note the difference from the classic "minimum window substring" (min_window_substring.py): there the
characters of t may appear in ANY order; here ORDER matters and duplicates count.

Hint (two pointers, O(|s| * |t|) worst case but fast in practice): scan s forward
matching t left-to-right; when the last char of t is matched at index `end`, walk
BACKWARD from `end` matching t right-to-left to find the latest possible `start`.
s[start:end+1] is a candidate; then resume the forward scan from start + 1.
(DP alternative: dp[j] = latest start index such that t[:j+1] is a subsequence of
s[start:i+1]; update j from high to low for each i.)

Run: python3 min_window_subsequence.py
"""


def min_window_subsequence(s, t):
    raise NotImplementedError


def _brute(s, t):
    if not t:
        return ""
    best = ""
    for i in range(len(s)):
        k = 0
        for j in range(i, len(s)):
            if s[j] == t[k]:
                k += 1
                if k == len(t):
                    if not best or j - i + 1 < len(best):
                        best = s[i:j + 1]
                    break
    return best


def _run_tests():
    assert min_window_subsequence("abcdebdde", "bde") == "bcde"
    assert min_window_subsequence("jmeqksfrsdcmsiwvaovztaqenprpvnbstl", "u") == ""
    assert min_window_subsequence("aaaa", "aa") == "aa"
    assert min_window_subsequence("fgrqsqsnodwmxzkzxwqegkndaa", "kzed") == "kzxwqegknd"
    assert min_window_subsequence("abc", "") == ""
    assert min_window_subsequence("", "a") == ""
    assert min_window_subsequence("abc", "abcd") == ""
    assert min_window_subsequence("abc", "cba") == ""
    assert min_window_subsequence("Abc", "abc") == ""
    assert min_window_subsequence("xyzabcxyzab", "ab") == "ab"
    assert min_window_subsequence("cnhczmccqouqadqtmjjzl", "mm") == "mccqouqadqtm"

    import random
    rng = random.Random(58)
    for _ in range(1500):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 14)))
        t = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
        assert min_window_subsequence(s, t) == _brute(s, t), (s, t)

    import time
    big = "".join(rng.choice("abcdefghij") for _ in range(200_000))
    t0 = time.time()
    res = min_window_subsequence(big, "jihgf")
    assert len(res) >= 5 and res[0] == "j" and res[-1] == "f"
    assert time.time() - t0 < 10, "too slow"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
