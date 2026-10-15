"""
Day 25, Task 9 -- CS fundamentals: longest common subsequence (DP).

THE PROBLEM
------------
A subsequence keeps the original order but may skip characters.

  lcs_length(a, b) -> length of the longest common subsequence.
  lcs(a, b)        -> ONE longest common subsequence as a string
                      (any valid one; the tests only check length and
                      that it is a subsequence of both inputs).

  lcs_length("ABCBDAB", "BDCABA") == 4     (e.g. "BCBA")

HOW TO WORK THROUGH THIS
-------------------------
dp[i][j] = LCS length of a[:i] and b[:j]. If a[i-1] == b[j-1] then
dp[i-1][j-1] + 1, else max(dp[i-1][j], dp[i][j-1]). To rebuild the string,
walk back from dp[len(a)][len(b)].

Run: python3 lcs.py
"""


def lcs_length(a: str, b: str) -> int:
    raise NotImplementedError


def lcs(a: str, b: str) -> str:
    raise NotImplementedError


def _is_subsequence(s: str, t: str) -> bool:
    it = iter(t)
    return all(ch in it for ch in s)


def _run_tests():
    assert lcs_length("", "abc") == 0
    assert lcs_length("abc", "") == 0
    assert lcs_length("abc", "abc") == 3
    assert lcs_length("abc", "def") == 0
    assert lcs_length("ABCBDAB", "BDCABA") == 4
    assert lcs_length("AGGTAB", "GXTXAYB") == 4
    for a, b in [("ABCBDAB", "BDCABA"), ("AGGTAB", "GXTXAYB"), ("abc", "abc"), ("abc", "def"), ("", "x")]:
        r = lcs(a, b)
        assert len(r) == lcs_length(a, b)
        assert _is_subsequence(r, a) and _is_subsequence(r, b)
    assert lcs("AGGTAB", "GXTXAYB") == "GTAB"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
