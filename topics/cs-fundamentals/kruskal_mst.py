"""
Day 26, Task 9 -- CS fundamentals: minimum spanning tree (Kruskal).

THE PROBLEM
------------
mst_weight(n, edges) takes n nodes (0..n-1) and a list of undirected
weighted edges (u, v, w). Return the total weight of a minimum spanning
tree, or None if the graph is not connected. A single node (n == 1) has
weight 0. Parallel edges and self-loops may appear; ignore self-loops.

HOW TO WORK THROUGH THIS
-------------------------
Sort edges by weight; add an edge if its endpoints are in different
components (union-find with path compression); stop after n-1 edges.
If fewer than n-1 edges were added, the graph is disconnected.

Run: python3 kruskal_mst.py
"""


def mst_weight(n: int, edges: list):
    raise NotImplementedError


def _run_tests():
    e = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4), (1, 3, 5)]
    assert mst_weight(4, e) == 7
    assert mst_weight(1, []) == 0
    assert mst_weight(3, [(0, 1, 5)]) is None
    e2 = [(0, 1, 10), (0, 1, 2), (1, 2, 3), (2, 3, 1), (3, 4, 7), (2, 4, 7)]
    assert mst_weight(5, e2) == 13
    assert mst_weight(2, [(0, 0, 1), (0, 1, 9)]) == 9
    assert mst_weight(3, []) is None
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
