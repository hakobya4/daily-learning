"""
Day 54, Task 10 -- Python: evaluate division (weighted graph / weighted union-find).

THE PROBLEM
------------
You are given equations like a / b = 2.0 as a list of (numerator, denominator) pairs plus a
parallel list of values, and a list of queries (x, y). For each query return x / y if it
can be derived from the equations, otherwise -1.0.

Rules:
  * Variables are strings. Every equation value is a positive float.
  * x / x is 1.0 ONLY if x appears in at least one equation; for an unknown variable
    (including x / x with x unknown) the answer is -1.0.
  * If x and y are both known but in disconnected groups, the answer is -1.0.
  * The equations are consistent (no contradictions).

Example: equations [("a","b"), ("b","c")], values [2.0, 3.0]
  queries ("a","c") -> 6.0, ("b","a") -> 0.5, ("a","e") -> -1.0, ("a","a") -> 1.0,
          ("x","x") -> -1.0

Hint (two valid approaches):
  1. Build a graph with an edge a->b of weight v and b->a of weight 1/v; answer each query
     with BFS/DFS multiplying weights along the path.
  2. Weighted union-find: parent[x] and weight[x] = x / parent[x]; find() compresses paths
     while multiplying weights; union(a, b, v) links the roots with the right ratio.
Raise ValueError if len(equations) != len(values).

Run: python3 evaluate_division.py
"""


def calc_equation(equations, values, queries):
    if len(equations) != len(values):
        raise ValueError("equations and values must have the same length")
    parent = {}
    weight = {}  # weight[x] = x / parent[x]

    def find(x):
        if parent[x] == x:
            return x, 1.0
        root, w = find(parent[x])
        parent[x] = root
        weight[x] *= w
        return root, weight[x]

    for (a, b), v in zip(equations, values):
        for x in (a, b):
            if x not in parent:
                parent[x] = x
                weight[x] = 1.0
        ra, wa = find(a)   # a = wa * ra
        rb, wb = find(b)   # b = wb * rb
        if ra != rb:
            # a / b = v  =>  ra / rb = v * wb / wa
            parent[ra] = rb
            weight[ra] = v * wb / wa

    out = []
    for x, y in queries:
        if x not in parent or y not in parent:
            out.append(-1.0)
            continue
        rx, wx = find(x)
        ry, wy = find(y)
        out.append(wx / wy if rx == ry else -1.0)
    return out


def _close(got, want):
    assert len(got) == len(want), (got, want)
    for g, w in zip(got, want):
        assert abs(g - w) < 1e-9, (got, want)


def _run_tests():
    _close(
        calc_equation([("a", "b"), ("b", "c")], [2.0, 3.0],
                      [("a", "c"), ("b", "a"), ("a", "e"), ("a", "a"), ("x", "x")]),
        [6.0, 0.5, -1.0, 1.0, -1.0],
    )
    _close(
        calc_equation([("a", "b"), ("b", "c"), ("bc", "cd")], [1.5, 2.5, 5.0],
                      [("a", "c"), ("c", "b"), ("bc", "cd"), ("cd", "bc")]),
        [3.75, 0.4, 5.0, 0.2],
    )
    # Two disconnected groups.
    _close(
        calc_equation([("a", "b"), ("c", "d")], [2.0, 4.0],
                      [("a", "d"), ("d", "c"), ("b", "a"), ("c", "c")]),
        [-1.0, 0.25, 0.5, 1.0],
    )
    # Longer chain, queried both ways, plus an edge that joins two previously built groups.
    eqs = [("x1", "x2"), ("x2", "x3"), ("x4", "x5"), ("x3", "x4")]
    vals = [3.0, 4.0, 5.0, 2.0]
    _close(
        calc_equation(eqs, vals, [("x1", "x5"), ("x5", "x1"), ("x2", "x4"), ("x5", "x3")]),
        [120.0, 1 / 120.0, 8.0, 0.1],
    )
    # No equations at all.
    _close(calc_equation([], [], [("a", "a"), ("a", "b")]), [-1.0, -1.0])
    # No queries.
    assert calc_equation([("a", "b")], [2.0], []) == []

    try:
        calc_equation([("a", "b")], [], [])
    except ValueError:
        pass
    else:
        raise AssertionError("mismatched lengths must raise ValueError")

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
