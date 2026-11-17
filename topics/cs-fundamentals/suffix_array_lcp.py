"""
Day 57, Task 4 -- CS fundamentals: suffix array (prefix doubling) + LCP array (Kasai).

THE PROBLEM
------------
Implement three functions over a string s:

1. suffix_array(s) -> list of the starting indices of all suffixes of s, sorted
   lexicographically (plain Python string order). suffix_array("") -> [].
   Do NOT just sort the suffix strings (that is O(n^2 log n)); use prefix doubling:
   rank[i] starts as ord(s[i]); in round k, sort indices by the pair
   (rank[i], rank[i + k] if i + k < n else -1), re-rank (equal pairs get equal ranks),
   double k, and stop as soon as all ranks are distinct. O(n log^2 n) with sort is fine.

2. lcp_array(s, sa) -> list `lcp` of len(sa) where lcp[0] = 0 and lcp[i] is the length
   of the longest common prefix of suffixes sa[i-1] and sa[i]. Use Kasai's algorithm:
   walk suffixes in TEXT order (i = 0..n-1) using rank[i] = position of i in sa, carry
   h over and decrement it by one at each step -- this makes it O(n).

3. Two applications using both arrays:
   * count_distinct_substrings(s) = n*(n+1)/2 - sum(lcp)   (non-empty substrings)
   * longest_repeated_substring(s) = the longest substring that occurs at least twice
     (occurrences may overlap); if several have the same max length return the
     lexicographically SMALLEST one; "" if none.

Example:
  suffix_array("banana")                  -> [5, 3, 1, 0, 4, 2]
  lcp_array("banana", [5, 3, 1, 0, 4, 2]) -> [0, 1, 3, 0, 0, 2]
  count_distinct_substrings("banana")     -> 15
  longest_repeated_substring("banana")    -> "ana"

Run: python3 suffix_array_lcp.py
"""


def suffix_array(s):
    n = len(s)
    if n == 0:
        return []
    rank = [ord(c) for c in s]
    sa = list(range(n))
    k = 1
    while True:
        key = lambda i: (rank[i], rank[i + k] if i + k < n else -1)
        sa.sort(key=key)
        new_rank = [0] * n
        for j in range(1, n):
            new_rank[sa[j]] = new_rank[sa[j - 1]] + (key(sa[j]) != key(sa[j - 1]))
        rank = new_rank
        if rank[sa[-1]] == n - 1:  # all ranks distinct
            break
        k *= 2
    return sa


def lcp_array(s, sa):
    n = len(s)
    if n == 0:
        return []
    rank = [0] * n
    for pos, i in enumerate(sa):
        rank[i] = pos
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


def count_distinct_substrings(s):
    n = len(s)
    return n * (n + 1) // 2 - sum(lcp_array(s, suffix_array(s)))


def longest_repeated_substring(s):
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    best_len, best_i = 0, -1
    for i, h in enumerate(lcp):
        if h > best_len:  # first max in suffix order = lexicographically smallest
            best_len, best_i = h, i
    return s[sa[best_i]:sa[best_i] + best_len] if best_len else ""


def _brute_lrs(s):
    best = ""
    n = len(s)
    for length in range(n - 1, 0, -1):
        seen, cands = set(), []
        for i in range(n - length + 1):
            sub = s[i:i + length]
            if sub in seen:
                cands.append(sub)
            seen.add(sub)
        if cands:
            return min(cands)
    return best


def _run_tests():
    assert suffix_array("banana") == [5, 3, 1, 0, 4, 2]
    assert lcp_array("banana", [5, 3, 1, 0, 4, 2]) == [0, 1, 3, 0, 0, 2]
    assert count_distinct_substrings("banana") == 15
    assert longest_repeated_substring("banana") == "ana"
    assert suffix_array("") == []
    assert lcp_array("", []) == []
    assert count_distinct_substrings("") == 0
    assert longest_repeated_substring("") == ""
    assert suffix_array("a") == [0]
    assert suffix_array("aaaa") == [3, 2, 1, 0]
    assert lcp_array("aaaa", [3, 2, 1, 0]) == [0, 1, 2, 3]
    assert count_distinct_substrings("aaaa") == 4
    assert longest_repeated_substring("aaaa") == "aaa"
    assert longest_repeated_substring("abcd") == ""
    assert longest_repeated_substring("abcabxab") == "ab"
    assert longest_repeated_substring("xyzxyabcab") == "ab"

    import random
    rng = random.Random(57)
    for _ in range(400):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 25)))
        exp_sa = sorted(range(len(s)), key=lambda i: s[i:])
        assert suffix_array(s) == exp_sa, s
        lcp = lcp_array(s, exp_sa)
        assert lcp[0] == 0
        for i in range(1, len(s)):
            a, b = s[exp_sa[i - 1]:], s[exp_sa[i]:]
            h = 0
            while h < min(len(a), len(b)) and a[h] == b[h]:
                h += 1
            assert lcp[i] == h, (s, i)
        distinct = {s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}
        assert count_distinct_substrings(s) == len(distinct), s
        assert longest_repeated_substring(s) == _brute_lrs(s), s

    # Efficiency: 100k chars, highly repetitive (the worst case for naive sorting).
    big = "ab" * 50_000
    sa = suffix_array(big)
    assert len(sa) == 100_000 and sa[0] == 99_998 and sa[-1] == 1
    assert longest_repeated_substring(big) == "ab" * 49_999
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
