"""
Day 52, Task 7 -- CS fundamentals: 2-D dynamic programming (interleaving string).

THE PROBLEM
------------
is_interleave(s1, s2, s3): return True if s3 can be formed by interleaving s1 and s2, i.e.
s3 is a merge of the characters of s1 and s2 that keeps the relative order of each string's
characters (like riffle-shuffling two decks of cards).
Examples: ("aabcc", "dbbca", "aadbbcbcac") -> True, ("aabcc", "dbbca", "aadbbbaccc") -> False,
("", "", "") -> True.
Hint: dp[i][j] = s3[:i+j] is an interleaving of s1[:i] and s2[:j]. Greedy fails when both
strings offer the same next character -- that is why you need the DP (or memoised recursion).
Bonus: reduce memory to one row of length len(s2) + 1.

Run: python3 interleaving_string.py
"""


def is_interleave(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    # dp[j]: s3[:i+j] is an interleaving of s1[:i] and s2[:j] (one row, reused per i)
    dp = [False] * (len(s2) + 1)
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i == 0 and j == 0:
                dp[j] = True
            else:
                from_s1 = i > 0 and dp[j] and s1[i - 1] == s3[i + j - 1]
                from_s2 = j > 0 and dp[j - 1] and s2[j - 1] == s3[i + j - 1]
                dp[j] = from_s1 or from_s2
    return dp[len(s2)]


def _run_tests():
    assert is_interleave("aabcc", "dbbca", "aadbbcbcac") is True
    assert is_interleave("aabcc", "dbbca", "aadbbbaccc") is False
    assert is_interleave("", "", "") is True
    assert is_interleave("", "abc", "abc") is True
    assert is_interleave("abc", "", "abd") is False
    assert is_interleave("a", "b", "ab") is True
    assert is_interleave("a", "b", "ba") is True
    assert is_interleave("ab", "cd", "abc") is False
    assert is_interleave("aa", "ab", "aaba") is True
    assert is_interleave("aa", "ab", "abaa") is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
