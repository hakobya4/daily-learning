"""
Day 59, Task 4 -- CS fundamentals: 2-SAT via the implication graph and SCCs.

THE PROBLEM
------------
Implement solve(n, clauses) -> list[bool] | None.

There are n boolean variables x1..xn. A literal is a non-zero int: +i means xi,
-i means NOT xi. Each clause is a pair (a, b) meaning (a OR b); a clause may repeat a
literal ((3, 3) forces x3 = True) or contain both polarities ((2, -2) is always true).
Return an assignment (index 0 -> x1) that makes EVERY clause true, or None if none
exists. A literal 0 or |literal| > n raises ValueError. n may be up to ~10^5 and the
clause list similarly long, so it must be linear time and must NOT recurse
(Python's recursion limit) -- no brute force.

Method:
  1. Nodes 2*(i-1) for xi and 2*(i-1)+1 for NOT xi (so negation is node ^ 1).
  2. Clause (a OR b) gives two implications: NOT a -> b and NOT b -> a.
  3. Compute strongly connected components (iterative Tarjan or Kosaraju).
  4. Unsatisfiable iff some xi and NOT xi are in the same SCC.
  5. Otherwise set xi = True iff comp(xi) comes AFTER comp(NOT xi) in a topological
     order of the condensation. (With Tarjan, components are numbered in REVERSE
     topological order, so that is: tarjan_id(xi) < tarjan_id(NOT xi).)

Examples:
  solve(3, [(1, 2), (-1, 3), (-2, -3)]) -> e.g. [True, False, True]
  solve(2, [(1, 2), (-1, 2), (1, -2), (-1, -2)]) -> None

Hint: an iterative DFS keeps an explicit stack of (node, next_edge_index). Write the
SCC part so you could reuse it -- `topics/cs-fundamentals/tarjan_scc.py` is the
recursive cousin of what you need here.

Run: python3 two_sat.py
"""


def _node(lit, n):
    if lit == 0 or abs(lit) > n:
        raise ValueError("literal out of range: %r" % (lit,))
    v = 2 * (abs(lit) - 1)
    return v if lit > 0 else v ^ 1


def _tarjan_iterative(num_nodes, adj):
    """Return comp[v]; components are numbered in reverse topological order."""
    index = [-1] * num_nodes
    low = [0] * num_nodes
    on_stack = [False] * num_nodes
    comp = [-1] * num_nodes
    stack = []
    counter = 0
    comp_count = 0
    for root in range(num_nodes):
        if index[root] != -1:
            continue
        work = [(root, 0)]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack[root] = True
        while work:
            v, ei = work[-1]
            edges = adj[v]
            if ei < len(edges):
                work[-1] = (v, ei + 1)
                w = edges[ei]
                if index[w] == -1:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack[w] = True
                    work.append((w, 0))
                elif on_stack[w] and index[w] < low[v]:
                    low[v] = index[w]
            else:
                work.pop()
                if work:
                    parent = work[-1][0]
                    if low[v] < low[parent]:
                        low[parent] = low[v]
                if low[v] == index[v]:
                    while True:
                        w = stack.pop()
                        on_stack[w] = False
                        comp[w] = comp_count
                        if w == v:
                            break
                    comp_count += 1
    return comp


def solve(n, clauses):
    adj = [[] for _ in range(2 * n)]
    for a, b in clauses:
        na, nb = _node(a, n), _node(b, n)
        adj[na ^ 1].append(nb)  # NOT a -> b
        adj[nb ^ 1].append(na)  # NOT b -> a
    comp = _tarjan_iterative(2 * n, adj)
    result = []
    for i in range(n):
        pos, neg = comp[2 * i], comp[2 * i + 1]
        if pos == neg:
            return None
        result.append(pos < neg)
    return result


def _satisfies(assign, clauses):
    return all(assign[abs(a) - 1] == (a > 0) or assign[abs(b) - 1] == (b > 0)
               for a, b in clauses)


def _run_tests():
    import itertools
    import random

    cl = [(1, 2), (-1, 3), (-2, -3)]
    res = solve(3, cl)
    assert res is not None and len(res) == 3 and _satisfies(res, cl)
    assert solve(2, [(1, 2), (-1, 2), (1, -2), (-1, -2)]) is None
    assert solve(1, [(1, 1)]) == [True]
    assert solve(1, [(-1, -1)]) == [False]
    assert solve(1, [(1, 1), (-1, -1)]) is None
    assert solve(1, [(1, -1)]) in ([True], [False])
    assert solve(4, []) is not None and len(solve(4, [])) == 4
    # chain x1 -> x2 -> ... -> x6, x1 forced true
    chain = [(-i, i + 1) for i in range(1, 6)] + [(1, 1)]
    assert solve(6, chain) == [True] * 6
    assert solve(6, chain + [(-6, -6)]) is None
    for bad in [[(0, 1)], [(1, 3)], [(-3, 1)]]:
        try:
            solve(2, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % bad)

    rng = random.Random(59)
    for _ in range(1500):
        n = rng.randint(1, 6)
        cls = [(rng.choice((1, -1)) * rng.randint(1, n), rng.choice((1, -1)) * rng.randint(1, n))
               for _ in range(rng.randint(0, 14))]
        res = solve(n, cls)
        brute = any(_satisfies(a, cls) for a in itertools.product((False, True), repeat=n))
        assert (res is not None) == brute, (n, cls, res)
        if res is not None:
            assert len(res) == n and _satisfies(res, cls), (n, cls, res)

    # large: long implication chain (would overflow a recursive DFS)
    n = 100_000
    big = [(-i, i + 1) for i in range(1, n)] + [(1, 1)]
    res = solve(n, big)
    assert res is not None and all(res)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
