"""
Day 27, Task 9 -- CS fundamentals: Bellman-Ford shortest paths.

THE PROBLEM
------------
bellman_ford(n, edges, source) -- nodes are 0..n-1, edges is a list of
(u, v, weight) DIRECTED edges; weights may be negative.

Return a list dist of length n with the shortest distance from source to
every node (float("inf") if unreachable). If a negative cycle is
reachable from source, return None.

HOW TO WORK THROUGH THIS
-------------------------
Relax every edge n-1 times (dist[v] = min(dist[v], dist[u] + w) when
dist[u] is finite). Do one more pass: if any edge still relaxes, there is
a reachable negative cycle. O(V*E).

Run: python3 bellman_ford.py
"""

INF = float("inf")


def bellman_ford(n: int, edges: list, source: int):
    dist = [INF] * n
    dist[source] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None
    return dist


def _run_tests():
    edges = [(0, 1, 4), (0, 2, 5), (1, 2, -3), (2, 3, 4)]
    assert bellman_ford(4, edges, 0) == [0, 4, 1, 5]
    assert bellman_ford(5, edges, 0) == [0, 4, 1, 5, INF]
    assert bellman_ford(1, [], 0) == [0]
    assert bellman_ford(3, [(0, 1, 2)], 1) == [INF, 0, INF]
    # negative cycle reachable from source
    assert bellman_ford(3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)], 0) is None
    # negative cycle NOT reachable from source
    assert bellman_ford(4, [(0, 1, 1), (2, 3, -2), (3, 2, 1)], 0) == [0, 1, INF, INF]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
