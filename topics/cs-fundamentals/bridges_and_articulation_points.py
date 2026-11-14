"""
Day 55, Task 3 -- CS fundamentals: bridges and articulation points (Tarjan low-link).

THE PROBLEM
------------
Given an UNDIRECTED graph with n vertices labelled 0..n-1 and a list of edges (u, v),
find:
  * bridges              -- edges whose removal increases the number of connected
                            components;
  * articulation points  -- vertices whose removal (with their edges) increases the number
                            of connected components.

Return (bridges, points) where
  * bridges is a sorted list of tuples (min(u, v), max(u, v)),
  * points  is a sorted list of vertex ids.

Rules:
  * The graph may be disconnected and may contain isolated vertices.
  * There are no self-loops, but there MAY be parallel edges: two copies of the edge (1, 2)
    mean that neither copy is a bridge. (So skip only the specific EDGE you arrived by,
    not every edge back to the parent -- track edge ids, not parent vertices.)
  * Raise ValueError for an edge endpoint outside 0..n-1 or a self-loop.

Hint: one DFS assigning disc[v] (discovery time) and low[v] = the smallest disc reachable
from v's subtree using at most one back edge.
  * Tree edge (u, v) is a bridge  iff  low[v] > disc[u].
  * Non-root u is an articulation point iff some child v has low[v] >= disc[u].
  * The DFS root is an articulation point iff it has >= 2 DFS children.
Use an ITERATIVE DFS (explicit stack) so a 100k-vertex path does not hit Python's
recursion limit. Overall O(n + m).

Run: python3 bridges_and_articulation_points.py
"""


def bridges_and_cut_vertices(n, edges):
    raise NotImplementedError


def _brute(n, edges):
    def components(vs_removed, edge_removed):
        adj = {v: [] for v in range(n) if v not in vs_removed}
        for i, (a, b) in enumerate(edges):
            if i == edge_removed or a in vs_removed or b in vs_removed:
                continue
            adj[a].append(b)
            adj[b].append(a)
        seen, c = set(), 0
        for s in adj:
            if s in seen:
                continue
            c += 1
            stack = [s]
            seen.add(s)
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
        return c

    base = components(set(), -1)
    br = sorted({(min(a, b), max(a, b)) for i, (a, b) in enumerate(edges)
                 if components(set(), i) > base})
    pts = []
    for v in range(n):
        deg = sum(1 for a, b in edges if v in (a, b))
        if deg == 0:
            continue
        if components({v}, -1) > base:
            pts.append(v)
    return br, pts


def _run_tests():
    # Classic example: triangle 0-1-2 with a tail 1-3-4.
    edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]
    assert bridges_and_cut_vertices(5, edges) == ([(1, 3), (3, 4)], [1, 3])

    # A simple path: every edge is a bridge, every inner vertex is a cut vertex.
    assert bridges_and_cut_vertices(4, [(0, 1), (1, 2), (2, 3)]) == (
        [(0, 1), (1, 2), (2, 3)], [1, 2])

    # A cycle has neither.
    assert bridges_and_cut_vertices(4, [(0, 1), (1, 2), (2, 3), (3, 0)]) == ([], [])

    # Parallel edges are not bridges, but the vertex can still be a cut vertex.
    assert bridges_and_cut_vertices(3, [(0, 1), (0, 1), (1, 2)]) == ([(1, 2)], [1])

    # Two triangles joined at vertex 2 (bow tie): 2 is a cut vertex, no bridges.
    bow = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)]
    assert bridges_and_cut_vertices(5, bow) == ([], [2])

    # Disconnected with isolated vertices; star centre is a cut vertex.
    star = [(0, 1), (0, 2), (0, 3), (5, 6)]
    assert bridges_and_cut_vertices(8, star) == ([(0, 1), (0, 2), (0, 3), (5, 6)], [0])
    assert bridges_and_cut_vertices(3, []) == ([], [])

    # Randomised cross-check against brute force (remove each edge / vertex, recount).
    import random
    rng = random.Random(55)
    for _ in range(300):
        n = rng.randint(1, 9)
        m = rng.randint(0, 12)
        es = []
        for _ in range(m):
            a, b = rng.randrange(n), rng.randrange(n)
            if a != b:
                es.append((a, b))
        assert bridges_and_cut_vertices(n, es) == _brute(n, es), (n, es)

    # Long path: no recursion-limit crash.
    n = 100_000
    path = [(i, i + 1) for i in range(n - 1)]
    br, pts = bridges_and_cut_vertices(n, path)
    assert len(br) == n - 1 and len(pts) == n - 2

    for bad in ([(0, 5)], [(1, 1)], [(-1, 0)]):
        try:
            bridges_and_cut_vertices(3, bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{bad} must raise ValueError")

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
