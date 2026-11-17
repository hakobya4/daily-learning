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


def _adjacency(n_left, edges):
    adj = [[] for _ in range(n_left)]
    seen = set()
    for u, v in edges:
        if (u, v) not in seen:
            seen.add((u, v))
            adj[u].append(v)
    return adj


def _kuhn(n_left, n_right, edges):
    """Iterative Kuhn's algorithm. Returns (adj, match_l, match_r)."""
    adj = _adjacency(n_left, edges)
    match_l = [-1] * n_left
    match_r = [-1] * n_right
    for root in range(n_left):
        visited_r = [False] * n_right
        # stack frames: [left vertex, next edge index, right vertex we came through]
        stack = [[root, 0, -1]]
        found = False
        while stack:
            frame = stack[-1]
            u, idx = frame[0], frame[1]
            if idx == len(adj[u]):
                stack.pop()
                continue
            v = adj[u][idx]
            frame[1] += 1
            if visited_r[v]:
                continue
            visited_r[v] = True
            if match_r[v] == -1:
                # augment along the stack: each frame's left vertex takes the right
                # vertex it just stepped to
                # rebuild path: frame i stepped to right vertex stack[i+1][2] (or v for last)
                for i in range(len(stack)):
                    lu = stack[i][0]
                    rv = stack[i + 1][2] if i + 1 < len(stack) else v
                    match_l[lu] = rv
                    match_r[rv] = lu
                found = True
                break
            stack.append([match_r[v], 0, v])
        if not found:
            continue
    return adj, match_l, match_r


def max_matching(n_left, n_right, edges):
    _, match_l, _ = _kuhn(n_left, n_right, edges)
    return [(u, v) for u, v in enumerate(match_l) if v != -1]


def min_vertex_cover(n_left, n_right, edges):
    adj, match_l, match_r = _kuhn(n_left, n_right, edges)
    z_left = set(u for u in range(n_left) if match_l[u] == -1)
    z_right = set()
    stack = list(z_left)
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v != match_l[u] and v not in z_right:
                z_right.add(v)
                w = match_r[v]
                if w != -1 and w not in z_left:
                    z_left.add(w)
                    stack.append(w)
    left_cover = set(range(n_left)) - z_left
    return left_cover, z_right


def max_independent_set_size(n_left, n_right, edges):
    return n_left + n_right - len(max_matching(n_left, n_right, edges))


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
