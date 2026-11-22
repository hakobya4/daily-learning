"""
Day 63, Task 4 -- CS fundamentals: random sampling algorithms -- reservoir sampling
(Algorithm R), weighted reservoir sampling (Efraimidis-Spirakis A-Res), and Walker/Vose
alias tables for O(1) weighted draws.

THE PROBLEM
------------
All functions take an explicit `rng` (a random.Random instance) and must use ONLY it --
never the global `random` module functions -- so results are reproducible.
Do not use random.sample / random.choices / numpy.

1) reservoir_sample(stream, k, rng) -> list
   Uniformly sample k items from an iterable of UNKNOWN length in one pass and O(k)
   memory (Algorithm R): keep the first k items; for the item with 0-based index i >= k,
   draw j = rng.randrange(i + 1) and, if j < k, replace reservoir[j] with it.
   If the stream has fewer than k items, return all of them (in stream order).
   k < 0 -> ValueError. Must work on generators (you cannot call len() on the stream).

2) weighted_reservoir_sample(stream, k, rng) -> list
   `stream` yields (item, weight) pairs with weight > 0 (weight <= 0 -> ValueError).
   Sample k DISTINCT items without replacement where, for k = 1, item i is chosen with
   probability w_i / sum(w). A-Res: give each item the key u ** (1 / w) with
   u = rng.random(), and keep the k items with the LARGEST keys using a min-heap of size
   k (heapq). Return the chosen items sorted by key, largest first. One pass, O(k) memory.
   (Why does u ** (1/w) work? Think about P(max of keys belongs to item i).)

3) class AliasTable(weights)
   Preprocess a list of non-negative weights (at least one > 0; otherwise or with any
   negative weight -> ValueError) in O(n) with Vose's method:
     scale p_i = w_i * n / sum(w); put indices with p_i < 1 in `small`, others in
     `large`; repeatedly pop s from small and l from large, set prob[s] = p_s,
     alias[s] = l, p_l -= (1 - p_s), and push l back onto small or large accordingly;
     whatever is left in either list gets prob = 1 (floating-point leftovers).
   Attributes: self.prob (list of floats in [0, 1]) and self.alias (list of ints),
   both of length n.
   - sample(rng) -> int: column = rng.randrange(n); return column if
     rng.random() < prob[column] else alias[column]. O(1).
   - probabilities() -> list of floats: reconstruct the EXACT distribution the table
     encodes: column c contributes prob[c] / n to c and (1 - prob[c]) / n to alias[c].
     This must equal w_i / sum(w) up to floating-point error -- the strongest test that
     your construction is right, independent of randomness.

Run: python3 reservoir_alias_sampling.py
"""

import heapq
import random


def reservoir_sample(stream, k, rng):
    raise NotImplementedError


def weighted_reservoir_sample(stream, k, rng):
    raise NotImplementedError


class AliasTable:
    def __init__(self, weights):
        raise NotImplementedError

    def sample(self, rng):
        raise NotImplementedError

    def probabilities(self):
        raise NotImplementedError


def _close(observed, expected_p, trials, sigmas=5.0):
    """True if a count is within `sigmas` standard deviations of a binomial mean."""
    mean = expected_p * trials
    sd = (trials * expected_p * (1 - expected_p)) ** 0.5
    return abs(observed - mean) <= sigmas * sd + 1e-9


def _run_tests():
    rng = random.Random(63)

    # --- reservoir sampling: basics ---
    assert reservoir_sample([], 3, rng) == []
    assert reservoir_sample([1, 2], 5, rng) == [1, 2]
    assert reservoir_sample(iter("abc"), 3, rng) == ["a", "b", "c"]
    assert reservoir_sample((x for x in range(10)), 0, rng) == []
    try:
        reservoir_sample([1], -1, rng)
    except ValueError:
        pass
    else:
        raise AssertionError("k < 0 must raise ValueError")
    s = reservoir_sample((x for x in range(1000)), 10, rng)
    assert len(s) == 10 and len(set(s)) == 10 and all(0 <= x < 1000 for x in s)

    # uses only the passed rng: same seed -> same sample
    a = reservoir_sample(range(500), 7, random.Random(1))
    random.seed(999)  # must not matter
    b = reservoir_sample(range(500), 7, random.Random(1))
    assert a == b

    # --- reservoir sampling: uniformity (each of 20 items picked with prob k/n) ---
    trials, n, k = 20000, 20, 5
    counts = [0] * n
    for _ in range(trials):
        for x in reservoir_sample(iter(range(n)), k, rng):
            counts[x] += 1
    for x in range(n):
        assert _close(counts[x], k / n, trials), (x, counts[x])

    # --- weighted reservoir ---
    try:
        weighted_reservoir_sample([("a", 1), ("b", 0)], 1, rng)
    except ValueError:
        pass
    else:
        raise AssertionError("weight <= 0 must raise ValueError")
    assert weighted_reservoir_sample([], 2, rng) == []
    got = weighted_reservoir_sample([("a", 1.0), ("b", 2.0)], 5, rng)
    assert sorted(got) == ["a", "b"]
    weights = {"x": 1.0, "y": 2.0, "z": 3.0, "w": 4.0}
    total = sum(weights.values())
    trials = 20000
    first = dict.fromkeys(weights, 0)
    for _ in range(trials):
        pick = weighted_reservoir_sample(iter(weights.items()), 1, rng)
        assert len(pick) == 1
        first[pick[0]] += 1
    for item, w in weights.items():
        assert _close(first[item], w / total, trials), (item, first[item])
    # k = 2: always distinct; the heaviest item is included more often than the lightest
    incl = dict.fromkeys(weights, 0)
    for _ in range(5000):
        pick = weighted_reservoir_sample(iter(weights.items()), 2, rng)
        assert len(pick) == 2 and len(set(pick)) == 2
        for p in pick:
            incl[p] += 1
    assert incl["w"] > incl["z"] > incl["y"] > incl["x"]
    # P(x in a 2-sample) = sum over first pick j != x of P(j) * P(x | j removed) ... = 0.2797
    p_x = sum((weights[j] / total) * (1.0 / (total - weights[j])) for j in weights if j != "x") + 0.1
    assert _close(incl["x"], p_x, 5000), (incl["x"], p_x)

    # --- alias tables ---
    for bad in ([], [0, 0], [1, -1]):
        try:
            AliasTable(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"AliasTable({bad}) must raise ValueError")
    for ws in ([1], [1, 1, 1, 1], [5, 0, 1], [0.1, 0.2, 0.7], [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
               [1e-9, 1, 1e9], list(range(1, 101))):
        t = AliasTable(ws)
        assert len(t.prob) == len(ws) == len(t.alias)
        assert all(0.0 <= p <= 1.0 + 1e-12 for p in t.prob)
        assert all(0 <= a < len(ws) for a in t.alias)
        tot = float(sum(ws))
        for got_p, w in zip(t.probabilities(), ws):
            assert abs(got_p - w / tot) < 1e-9, (ws, got_p, w / tot)
    t = AliasTable([5, 0, 1])
    assert all(t.sample(rng) != 1 for _ in range(5000))     # zero weight is never drawn
    ws = [3, 1, 4, 1, 5, 9, 2, 6]
    t = AliasTable(ws)
    trials = 40000
    counts = [0] * len(ws)
    for _ in range(trials):
        counts[t.sample(rng)] += 1
    for i, w in enumerate(ws):
        assert _close(counts[i], w / sum(ws), trials), (i, counts[i])
    big = AliasTable([rng.random() for _ in range(200000)])   # O(n) build must be quick
    assert len(big.prob) == 200000

    print("all sampling tests passed")


if __name__ == "__main__":
    _run_tests()
