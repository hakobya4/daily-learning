"""
Day 31, Task 10 -- CS fundamentals: Floyd-Warshall all-pairs shortest paths.

THE PROBLEM
------------
Graph: n nodes (0..n-1) and a list of directed edges (u, v, weight);
weights may be negative.

  floyd_warshall(n, edges) -> n x n matrix dist where dist[i][j] is the
      shortest path length from i to j, dist[i][i] == 0, and
      float('inf') when j is unreachable from i. (Assume no negative cycle.)
  has_negative_cycle(n, edges) -> True if the graph has a negative-weight
      cycle (after running the algorithm some dist[i][i] < 0).

HOW TO WORK THROUGH THIS
-------------------------
Initialise dist with inf, 0 on the diagonal, and the smallest weight for
parallel edges. Then three nested loops with k OUTERMOST:
dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]).
Skip the update when dist[i][k] or dist[k][j] is inf. For has_negative_cycle
reuse the same loops and check the diagonal.

Run: python3 floyd_warshall.py
"""

INF = float("inf")


def floyd_warshall(n: int, edges: list) -> list:
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[k][j] == INF:
                    continue
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def has_negative_cycle(n: int, edges: list) -> bool:
    dist = floyd_warshall(n, edges)
    return any(dist[i][i] < 0 for i in range(n))


def _run_tests():
    d = floyd_warshall(4, [(0, 1, 5), (1, 2, 3), (2, 3, 1), (0, 3, 10)])
    assert d[0][3] == 9
    assert d[0][2] == 8
    assert d[3][0] == INF
    assert d[2][2] == 0
    assert d[1][3] == 4

    d = floyd_warshall(3, [(0, 1, -2), (1, 2, 3), (0, 2, 5)])
    assert d[0][2] == 1
    assert d[2][0] == INF

    d = floyd_warshall(2, [(0, 1, 7), (0, 1, 3)])   # parallel edges
    assert d[0][1] == 3

    assert floyd_warshall(1, []) == [[0]]

    assert has_negative_cycle(3, [(0, 1, 1), (1, 2, -3), (2, 0, 1)]) is True
    assert has_negative_cycle(4, [(0, 1, 5), (1, 2, 3), (2, 3, 1), (0, 3, 10)]) is False
    assert has_negative_cycle(3, [(0, 1, -2), (1, 2, 3), (0, 2, 5)]) is False
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
