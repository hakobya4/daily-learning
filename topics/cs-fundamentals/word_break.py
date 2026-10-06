"""
Day 15, Task 8 -- CS fundamentals: word break (dynamic programming).

THE PROBLEM
------------
Given a string s and a list of words, decide whether s can be split into
a sequence of dictionary words (words reusable).

    can_break("leetcode", ["leet", "code"])            -> True
    can_break("applepenapple", ["apple", "pen"])       -> True
    can_break("catsandog", ["cats","dog","sand","and","cat"]) -> False
    can_break("", [...])                               -> True

Also implement all_breaks(s, words) -> every valid sentence (words joined
by single spaces) as a sorted list:

    all_breaks("catsanddog", ["cat","cats","and","sand","dog"])
        -> ["cat sand dog", "cats and dog"]

can_break must be O(n * L) or O(n^2), NOT exponential: it must answer
"a"*40 + "b" with words ["a","aa","aaa"] instantly.

HOW TO WORK THROUGH THIS
-------------------------
dp[i] = True if s[:i] can be broken; dp[0] = True; dp[i] is true if some
j < i has dp[j] and s[j:i] in the word set. For all_breaks use
memoized recursion on the start index.

Run: python3 word_break.py
"""


def can_break(s: str, words: list[str]) -> bool:
    word_set = set(words)
    lengths = {len(w) for w in word_set}
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for L in lengths:
            if L <= i and dp[i - L] and s[i - L:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]


def all_breaks(s: str, words: list[str]) -> list[str]:
    word_set = set(words)
    memo: dict[int, list[str]] = {}

    def go(start: int) -> list[str]:
        if start == len(s):
            return [""]
        if start in memo:
            return memo[start]
        out = []
        for end in range(start + 1, len(s) + 1):
            w = s[start:end]
            if w in word_set:
                for rest in go(end):
                    out.append(w if rest == "" else w + " " + rest)
        memo[start] = out
        return out

    return sorted(go(0))


def _run_tests() -> None:
    assert can_break("leetcode", ["leet", "code"]) is True
    assert can_break("applepenapple", ["apple", "pen"]) is True
    assert can_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    assert can_break("", ["a"]) is True
    assert can_break("a", []) is False
    assert can_break("a" * 40 + "b", ["a", "aa", "aaa"]) is False
    assert all_breaks("catsanddog", ["cat", "cats", "and", "sand", "dog"]) == [
        "cat sand dog",
        "cats and dog",
    ]
    assert all_breaks("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]) == [
        "pine apple pen apple",
        "pine applepen apple",
        "pineapple pen apple",
    ]
    assert all_breaks("catsandog", ["cats", "dog", "sand", "and", "cat"]) == []
    assert all_breaks("", ["a"]) == [""]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
