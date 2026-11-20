"""
Day 60, Task 4 -- CS fundamentals: the assignment problem with the Hungarian algorithm.

THE PROBLEM
------------
cost is an n x m matrix (list of lists of ints, n <= m): cost[i][j] is the cost of giving
job j to worker i. Every worker must get exactly ONE job and no job may be given twice
(with m > n some jobs stay unused). Minimise the total cost.

Implement assign(cost) -> (total, match) where match[i] is the column given to row i
(a list of n DISTINCT column indices) and total == sum(cost[i][match[i]]).
  - assign([]) -> (0, []).
  - Costs may be negative or zero.
  - Raise ValueError if the rows have different lengths, or n > m.
  - If several optimal matchings exist, any of them is accepted.

It must run in O(n^2 * m) -- the 200 x 200 test must finish in a couple of seconds, so
trying all n! permutations (or a plain DFS) is out.

Example:
  assign([[4, 1, 3],
          [2, 0, 5],
          [3, 2, 2]])  -> (5, [1, 0, 2])        1 + 2 + 2

Hint: the "potentials" version (often called the e-maxx / Jonker-style O(n^2 m)
Hungarian): keep row potentials u, column potentials v, and for each new row run a
Dijkstra-like scan over columns with minv[j] = min reduced cost cost[i][j] - u[i] - v[j]
seen so far and way[j] = previous column on the alternating path; when a free column is
reached, flip the path. Use 1-based indices with a dummy column 0 to keep it short.
Alternative for practice: min-cost max-flow with Bellman-Ford/SPFA (slower, still OK).

Run: python3 hungarian_assignment.py
"""


def assign(cost):
    n = len(cost)
    if n == 0:
        return 0, []
    m = len(cost[0])
    if any(len(row) != m for row in cost):
        raise ValueError("rows have different lengths")
    if n > m:
        raise ValueError("more rows than columns")
    INF = float("inf")
    # 1-based: u[0..n], v[0..m]; p[j] = row matched to column j (0 = free)
    u = [0] * (n + 1)
    v = [0] * (m + 1)
    p = [0] * (m + 1)
    way = [0] * (m + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            row = cost[i0 - 1]
            ui0 = u[i0]
            delta = INF
            j1 = 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = row[j - 1] - ui0 - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        # flip the alternating path
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    match = [0] * n
    for j in range(1, m + 1):
        if p[j]:
            match[p[j] - 1] = j - 1
    total = sum(cost[i][match[i]] for i in range(n))
    return total, match


def _brute(cost):
    from itertools import permutations
    n = len(cost)
    m = len(cost[0]) if n else 0
    best = None
    for perm in permutations(range(m), n):
        s = sum(cost[i][perm[i]] for i in range(n))
        if best is None or s < best:
            best = s
    return 0 if best is None else best


def _check(cost, total, match):
    n = len(cost)
    assert len(match) == n
    assert len(set(match)) == n, match
    assert all(0 <= j < len(cost[0]) for j in match)
    assert total == sum(cost[i][match[i]] for i in range(n)), (total, match)


def _run_tests():
    import random
    import time

    assert assign([]) == (0, [])
    assert assign([[7]]) == (7, [0])
    c = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]
    total, match = assign(c)
    _check(c, total, match)
    assert total == 5 and match == [1, 0, 2]
    c = [[1, 2, 3, 4]]
    assert assign(c) == (1, [0])
    c = [[10, 10, 1], [10, 1, 10]]
    total, match = assign(c)
    _check(c, total, match)
    assert total == 2 and match == [2, 1]
    c = [[-5, 0], [0, -5]]
    assert assign(c)[0] == -10
    c = [[3, 3], [3, 3]]
    total, match = assign(c)
    _check(c, total, match)
    assert total == 6

    rng = random.Random(60)
    for _ in range(300):
        n = rng.randint(1, 6)
        m = rng.randint(n, 7)
        c = [[rng.randint(-20, 50) for _ in range(m)] for _ in range(n)]
        total, match = assign(c)
        _check(c, total, match)
        assert total == _brute(c), (c, total)

    # a known optimum: a permutation of zeros hidden among costs >= 1
    n = 200
    perm = list(range(n))
    rng.shuffle(perm)
    c = [[rng.randint(1, 1000) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        c[i][perm[i]] = 0
    t0 = time.time()
    total, match = assign(c)
    elapsed = time.time() - t0
    _check(c, total, match)
    assert total == 0 and match == perm
    assert elapsed < 5, "too slow: %.1fs" % elapsed

    for bad in ([[1, 2], [3]], [[1], [2]]):
        try:
            assign(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
