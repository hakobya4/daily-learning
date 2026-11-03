"""
Day 43, Task 9 -- CS fundamentals: maximum flow (Edmonds-Karp).

THE PROBLEM
------------
max_flow(n, edges, s, t) -> int
n nodes 0..n-1; edges is a list of (u, v, capacity) DIRECTED edges (parallel
edges allowed, their capacities add up). Return the maximum flow from s to t.
Edmonds-Karp: repeat BFS on the residual graph to find a shortest augmenting
path, push the bottleneck capacity along it, update residual capacities
(forward -= f, backward += f). Stop when t is unreachable.
If s == t return 0.

Run: python3 max_flow_edmonds_karp.py
"""


def max_flow(n, edges, s, t):
    from collections import deque, defaultdict
    if s == t:
        return 0
    cap = defaultdict(int)
    adj = [set() for _ in range(n)]
    for u, v, c in edges:
        cap[(u, v)] += c
        adj[u].add(v)
        adj[v].add(u)
    flow = 0
    while True:
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v in adj[u]:
                if v not in parent and cap[(u, v)] > 0:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            return flow
        b = float("inf")
        v = t
        while parent[v] is not None:
            b = min(b, cap[(parent[v], v)])
            v = parent[v]
        v = t
        while parent[v] is not None:
            u = parent[v]
            cap[(u, v)] -= b
            cap[(v, u)] += b
            v = u
        flow += b


def _run_tests():
    clrs = [(0, 1, 16), (0, 2, 13), (1, 2, 10), (2, 1, 4), (1, 3, 12),
            (3, 2, 9), (2, 4, 14), (4, 3, 7), (3, 5, 20), (4, 5, 4)]
    assert max_flow(6, clrs, 0, 5) == 23
    assert max_flow(2, [(0, 1, 5)], 0, 1) == 5
    assert max_flow(3, [(0, 1, 3), (0, 1, 2), (1, 2, 4)], 0, 2) == 4
    assert max_flow(3, [(0, 1, 3)], 0, 2) == 0
    assert max_flow(3, [(0, 1, 3), (1, 2, 3)], 1, 1) == 0
    # needs a backward residual edge to reach the optimum (2)
    diamond = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
    assert max_flow(4, diamond, 0, 3) == 2
    # edge direction matters
    assert max_flow(2, [(1, 0, 9)], 0, 1) == 0
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
