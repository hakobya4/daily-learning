"""
Day 57, Task 10 -- Python: word wrap with minimum raggedness (DP, not greedy).

THE PROBLEM
------------
Given a list of words (each non-empty, no spaces) and a line width W, split the words,
in order, into lines. A line holding words i..j has length
    sum(len(words[i..j])) + (j - i)          (single spaces between words)
which must be <= W. If any single word is longer than W, raise ValueError.

The cost of a line is (W - length) ** 2, EXCEPT the LAST line, which costs 0.
Return the wrapping that minimises the total cost:

    wrap_min_raggedness(words, W) -> (cost, lines)

where lines is a list of strings (words joined by single spaces). If several wrappings
tie on cost, return the one whose list of line lengths is lexicographically LARGEST
(i.e. prefer filling earlier lines more). Empty input -> (0, []).

Example:
  words = "aaa bb cc ddddd".split(), W = 6
  greedy wraps  "aaa bb" / "cc" / "ddddd"  -> cost 0 + 16 + 0 = 16
  optimal is    "aaa" / "bb cc" / "ddddd"  -> cost 9 + 1 + 0 = 10
  wrap_min_raggedness(words, 6) -> (10, ["aaa", "bb cc", "ddddd"])

Also implement greedy_wrap(words, W) -> lines (pack as many words as fit on each line),
which the tests use to show the DP is never worse than greedy.

Hint: dp[i] = minimal cost to wrap words[i:]; dp[n] = 0. For each i try every j >= i
while words i..j still fit: cost = 0 if j == n-1 else (W - len)**2, plus dp[j+1].
Iterating j upward and keeping the first strictly-better j does NOT give the tie-break
above -- think about which j to prefer on equal cost. O(n * W) because a line holds at
most (W+1)//2 words.

Run: python3 min_raggedness_wrap.py
"""


def greedy_wrap(words, W):
    raise NotImplementedError


def wrap_min_raggedness(words, W):
    raise NotImplementedError


def _cost(lines, W):
    return sum((W - len(l)) ** 2 for l in lines[:-1])


def _all_wraps(words, W):
    n = len(words)
    if n == 0:
        yield []
        return
    for mask in range(1 << (n - 1)):
        lines, cur = [], [words[0]]
        for i in range(1, n):
            if mask >> (i - 1) & 1:
                lines.append(" ".join(cur))
                cur = [words[i]]
            else:
                cur.append(words[i])
        lines.append(" ".join(cur))
        if all(len(l) <= W for l in lines):
            yield lines


def _brute(words, W):
    best = None
    for lines in _all_wraps(words, W):
        key = (_cost(lines, W), [-len(l) for l in lines])
        if best is None or key < best[0]:
            best = (key, lines)
    return best[0][0], best[1]


def _run_tests():
    assert wrap_min_raggedness("aaa bb cc ddddd".split(), 6) == (10, ["aaa", "bb cc", "ddddd"])
    assert greedy_wrap("aaa bb cc ddddd".split(), 6) == ["aaa bb", "cc", "ddddd"]
    assert wrap_min_raggedness([], 10) == (0, [])
    assert greedy_wrap([], 10) == []
    assert wrap_min_raggedness(["hello"], 5) == (0, ["hello"])
    assert wrap_min_raggedness(["a", "b", "c"], 5) == (0, ["a b c"])
    assert wrap_min_raggedness(["ab", "cd", "e"], 5) == (0, ["ab cd", "e"])
    # real tie (cost 14 both ways): "ab" / "c de" / ...  vs  "ab c" / "de" / ...
    # -> line lengths [2, 4, 3, 3] vs [4, 2, 3, 3]: prefer the lexicographically larger
    assert wrap_min_raggedness(["ab", "c", "de", "fgh", "ijk"], 5) == \
        (14, ["ab c", "de", "fgh", "ijk"])
    try:
        wrap_min_raggedness(["toolongword"], 5)
        assert False, "expected ValueError"
    except ValueError:
        pass
    try:
        greedy_wrap(["toolongword"], 5)
        assert False, "expected ValueError"
    except ValueError:
        pass

    import random
    rng = random.Random(57)
    for _ in range(400):
        W = rng.randint(4, 14)
        words = ["x" * rng.randint(1, min(W, 6)) for _ in range(rng.randint(1, 10))]
        exp = _brute(words, W)
        got = wrap_min_raggedness(words, W)
        assert got == exp, (words, W, got, exp)
        g = greedy_wrap(words, W)
        assert " ".join(g) == " ".join(words) and all(len(l) <= W for l in g)
        assert got[0] <= _cost(g, W)

    # Efficiency: 20k words, width 80.
    big = ["w" * rng.randint(1, 12) for _ in range(20_000)]
    cost, lines = wrap_min_raggedness(big, 80)
    assert " ".join(lines) == " ".join(big) and all(len(l) <= 80 for l in lines)
    assert cost <= _cost(greedy_wrap(big, 80), 80)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
