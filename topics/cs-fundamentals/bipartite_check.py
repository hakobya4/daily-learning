"""
Day 28, Task 9 -- CS fundamentals: is the graph bipartite?

THE PROBLEM
------------
is_bipartite(n, edges) -> bool. The graph has nodes 0..n-1 and undirected
edges given as (u, v) pairs. It is bipartite if the nodes can be split
into two sets so that every edge joins nodes from different sets
(equivalently: it has no odd-length cycle). The graph may be
disconnected; isolated nodes are fine.

  is_bipartite(4, [(0,1),(1,2),(2,3),(3,0)]) -> True   (even cycle)
  is_bipartite(3, [(0,1),(1,2),(2,0)])       -> False  (triangle)

HOW TO WORK THROUGH THIS
-------------------------
BFS/DFS 2-colouring from every unvisited node; if an edge ever joins two
nodes of the same colour, return False. Self-loops (u == v) make a graph
non-bipartite.

Run: python3 bipartite_check.py
"""


def is_bipartite(n: int, edges: list) -> bool:
    raise NotImplementedError


def _run_tests():
    assert is_bipartite(0, []) is True
    assert is_bipartite(1, []) is True
    assert is_bipartite(4, [(0, 1), (1, 2), (2, 3), (3, 0)]) is True
    assert is_bipartite(3, [(0, 1), (1, 2), (2, 0)]) is False
    assert is_bipartite(5, [(0, 1), (3, 4)]) is True           # disconnected
    assert is_bipartite(6, [(0, 1), (1, 2), (3, 4), (4, 5), (5, 3)]) is False  # bad 2nd component
    assert is_bipartite(2, [(0, 0)]) is False                  # self-loop
    assert is_bipartite(5, [(0, 1), (0, 2), (0, 3), (0, 4)]) is True  # star
    assert is_bipartite(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]) is False  # 5-cycle
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
