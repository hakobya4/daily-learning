"""
Day 57, Task 7 -- CS fundamentals: maximum bipartite matching + Koenig's minimum vertex cover.

THE PROBLEM
------------
A bipartite graph has left vertices 0..n_left-1, right vertices 0..n_right-1 and an edge
list `edges` of (u, v) pairs (u on the left, v on the right; duplicates possible).

1. max_matching(n_left, n_right, edges) -> list of (u, v) pairs forming a MAXIMUM
   matching (no vertex used twice, every pair is an edge), sorted by u.
   Use augmenting paths: Kuhn's algorithm (DFS from each free left vertex, O(V*E)) is
   enough for the tests if written ITERATIVELY or with a raised recursion limit;
   Hopcroft-Karp (BFS layers + DFS, O(E*sqrt(V))) is the bonus.

2. min_vertex_cover(n_left, n_right, edges) -> (left_set, right_set), two Python sets
   whose union touches every edge and whose total size equals the matching size
   (Koenig's theorem). Construction: from every UNMATCHED left vertex, run an
   alternating search (left -> right via any non-matching edge, right -> left via the
   matching edge). Let Z be all vertices reached. Then cover = (L \\ Z) | (R & Z).

3. max_independent_set_size(n_left, n_right, edges) = n_left + n_right - matching size.

Example:
  edges = [(0, 0), (0, 1), (1, 0), (2, 1), (2, 2)]
  len(max_matching(3, 3, edges))        -> 3
  max_matching(2, 2, [(0, 0), (1, 0)])  -> [(0, 0)] or [(1, 0)]   (size 1)
  min_vertex_cover(2, 2, [(0, 0), (1, 0)]) -> (set(), {0})

Run: python3 bipartite_matching.py
"""


def max_matching(n_left, n_right, edges):
    raise NotImplementedError


def min_vertex_cover(n_left, n_right, edges):
    raise NotImplementedError


def max_independent_set_size(n_left, n_right, edges):
    raise NotImplementedError


def _brute_matching_size(edges):
    edges = sorted(set(edges))
    best = 0

    def go(i, used_l, used_r, size):
        nonlocal best
        best = max(best, size)
        if i == len(edges) or size + (len(edges) - i) <= best:
            return
        u, v = edges[i]
        if u not in used_l and v not in used_r:
            go(i + 1, used_l | {u}, used_r | {v}, size + 1)
        go(i + 1, used_l, used_r, size)

    go(0, frozenset(), frozenset(), 0)
    return best


def _check(n_left, n_right, edges, expected_size):
    m = max_matching(n_left, n_right, edges)
    es = set(edges)
    assert len(m) == expected_size, (edges, m)
    assert m == sorted(m)
    assert all(e in es for e in m)
    assert len({u for u, _ in m}) == len(m) and len({v for _, v in m}) == len(m)
    L, R = min_vertex_cover(n_left, n_right, edges)
    assert len(L) + len(R) == expected_size, (edges, L, R)
    assert all(u in L or v in R for u, v in edges), (edges, L, R)
    assert max_independent_set_size(n_left, n_right, edges) == n_left + n_right - expected_size


def _run_tests():
    _check(3, 3, [(0, 0), (0, 1), (1, 0), (2, 1), (2, 2)], 3)
    _check(2, 2, [(0, 0), (1, 0)], 1)
    assert min_vertex_cover(2, 2, [(0, 0), (1, 0)]) == (set(), {0})
    _check(3, 2, [], 0)
    assert max_matching(0, 0, []) == []
    _check(4, 4, [(0, 0), (0, 0), (1, 1), (2, 2), (3, 3)], 4)
    # needs a real augmenting path, greedy fails
    _check(2, 2, [(0, 0), (0, 1), (1, 0)], 2)

    import random
    rng = random.Random(57)
    for _ in range(300):
        nl, nr = rng.randint(1, 6), rng.randint(1, 6)
        edges = [(rng.randrange(nl), rng.randrange(nr)) for _ in range(rng.randint(0, 12))]
        _check(nl, nr, edges, _brute_matching_size(edges))

    # Size: a chain where the LAST left vertex needs an augmenting path through all the
    # others (u_i greedily takes v_i first; u_{n-1} only knows v_0) -- recursion depth!
    n = 3000
    chain = []
    for i in range(n - 1):
        chain += [(i, i), (i, i + 1)]
    chain.append((n - 1, 0))
    assert len(max_matching(n, n, chain)) == n
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
