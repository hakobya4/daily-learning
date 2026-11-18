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


def solve(n, clauses):
    raise NotImplementedError


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
