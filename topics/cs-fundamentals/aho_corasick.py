"""
Day 58, Task 4 -- CS fundamentals: Aho-Corasick multi-pattern string search.

THE PROBLEM
------------
Searching a text for k patterns one at a time (KMP / Z / Rabin-Karp, all done on
earlier days) costs O(k * n). Aho-Corasick builds ONE automaton over all patterns and
finds every occurrence of every pattern in a single pass: O(n + total_pattern_length +
number_of_matches).

Implement:

  class AhoCorasick:
      __init__(self, patterns)   # list of non-empty strings; duplicates allowed
      find_all(self, text) -> list of (start_index, pattern_index)
          every occurrence of every pattern (overlaps included), sorted by
          start_index, then by pattern_index. A duplicated pattern reports every one
          of its indices.
      count(self, text) -> list of ints, count[i] = occurrences of patterns[i]

  first_match(patterns, text) -> (start_index, pattern_index) or None
      the occurrence that ENDS earliest in the text (ties: the longer pattern, i.e.
      the smaller start; then the smaller pattern_index). Use the automaton, and stop
      scanning as soon as you know the answer.

ValueError if any pattern is empty. An empty patterns list is allowed (no matches).

Example:
  ac = AhoCorasick(["he", "she", "his", "hers"])
  ac.find_all("ushers") -> [(1, 1), (2, 0), (2, 3)]   # "she"@1, "he"@2, "hers"@2
  ac.count("ushers he") -> [2, 1, 0, 1]
  first_match(["he", "she", "his", "hers"], "ushers") -> (1, 1)   # "she" ends at 3, as does "he": longer wins

Hint:
  1. Build a trie: goto[state] = {char: next_state}; out[state] = list of pattern
     indices ending exactly at this state.
  2. BFS from the root to compute fail[state] = the state for the longest proper
     suffix of this state's string that is also a trie prefix. For child c of state u:
     follow f = fail[u] until f has a c-edge (or f is the root); fail[child] = goto[f][c]
     (or root). Then out-links: dict_link[child] = fail[child] if out[fail[child]] else
     dict_link[fail[child]] -- so reporting a match walks only states that have outputs.
  3. Scan: from the current state follow fail links until a c-edge exists; at each
     position report out[state] and all outputs along the dict_link chain. A match of
     pattern p ending at i starts at i - len(p) + 1.

Run: python3 aho_corasick.py
"""


class AhoCorasick:
    def __init__(self, patterns):
        raise NotImplementedError

    def find_all(self, text):
        raise NotImplementedError

    def count(self, text):
        raise NotImplementedError


def first_match(patterns, text):
    raise NotImplementedError


def _brute(patterns, text):
    res = []
    for i in range(len(text)):
        for j, p in enumerate(patterns):
            if text.startswith(p, i):
                res.append((i, j))
    return res


def _brute_first(patterns, text):
    best = None
    for s, j in _brute(patterns, text):
        key = (s + len(patterns[j]) - 1, s, j)
        if best is None or key < best:
            best = key
    return None if best is None else (best[1], best[2])


def _run_tests():
    pats = ["he", "she", "his", "hers"]
    ac = AhoCorasick(pats)
    assert ac.find_all("ushers") == [(1, 1), (2, 0), (2, 3)]
    assert ac.count("ushers he") == [2, 1, 0, 1]
    assert first_match(pats, "ushers") == (1, 1)
    assert ac.find_all("") == []
    assert ac.find_all("xyz") == []
    assert first_match(pats, "xyz") is None

    ac2 = AhoCorasick(["a", "aa", "aaa", "a"])
    assert ac2.find_all("aaa") == [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1),
                                   (1, 3), (2, 0), (2, 3)]
    assert ac2.count("aaaa") == [4, 3, 2, 4]
    assert first_match(["a", "aa", "aaa", "a"], "baaa") == (1, 0)
    assert first_match(["bc", "abc", "c"], "xabcd") == (1, 1)

    assert AhoCorasick([]).find_all("abc") == []
    assert AhoCorasick([]).count("abc") == []
    try:
        AhoCorasick(["ok", ""])
    except ValueError:
        pass
    else:
        raise AssertionError("empty pattern must raise ValueError")

    import random
    rng = random.Random(58)
    for _ in range(1000):
        pats = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
                for _ in range(rng.randint(1, 6))]
        text = "".join(rng.choice("abc") for _ in range(rng.randint(0, 25)))
        ac = AhoCorasick(pats)
        exp = _brute(pats, text)
        assert ac.find_all(text) == exp, (pats, text)
        assert ac.count(text) == [sum(1 for _, j in exp if j == i) for i in range(len(pats))]
        assert first_match(pats, text) == _brute_first(pats, text), (pats, text)

    # one pass, not k passes: 2000 patterns over a 200k text
    import time
    alphabet = "abcdefgh"
    pats = ["".join(rng.choice(alphabet) for _ in range(rng.randint(3, 8))) for _ in range(2000)]
    text = "".join(rng.choice(alphabet) for _ in range(200_000))
    t0 = time.time()
    total = sum(AhoCorasick(pats).count(text))
    assert total > 0
    assert time.time() - t0 < 10, "too slow -- one automaton, one pass"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
