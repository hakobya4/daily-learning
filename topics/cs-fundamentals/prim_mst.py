"""
Day 30, Task 10 -- CS fundamentals: Prim's minimum spanning tree.

THE PROBLEM
------------
prim_mst(n, edges) -> total weight of a minimum spanning tree of the
undirected weighted graph with vertices 0..n-1, where edges is a list of
(u, v, w). If the graph is not connected return None. n == 0 or n == 1
gives 0.

  n=4, edges=[(0,1,1),(1,2,2),(2,3,3),(0,3,10),(0,2,4)] -> 6

HOW TO WORK THROUGH THIS
-------------------------
Build an adjacency list. Start at vertex 0, push its edges on a heap
(weight, vertex); pop the cheapest edge to an unvisited vertex, add its
weight, push that vertex's edges. Done when n vertices are visited; if the
heap empties first the graph is disconnected.

Run: python3 prim_mst.py
"""
import heapq  # noqa: F401  (hint: you will want it)


def prim_mst(n: int, edges: list):
    raise NotImplementedError


def _run_tests():
    assert prim_mst(4, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10), (0, 2, 4)]) == 6
    assert prim_mst(0, []) == 0
    assert prim_mst(1, []) == 0
    assert prim_mst(2, []) is None
    assert prim_mst(3, [(0, 1, 5)]) is None
    assert prim_mst(2, [(0, 1, 7), (0, 1, 3)]) == 3
    assert prim_mst(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)]) == 2
    edges = [(0, 1, 4), (0, 7, 8), (1, 2, 8), (1, 7, 11), (2, 3, 7), (2, 8, 2),
             (2, 5, 4), (3, 4, 9), (3, 5, 14), (4, 5, 10), (5, 6, 2), (6, 7, 1),
             (6, 8, 6), (7, 8, 7)]
    assert prim_mst(9, edges) == 37
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
