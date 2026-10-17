"""
Day 27, Task 10 -- CS fundamentals: cycle detection in a directed graph.

THE PROBLEM
------------
has_cycle(n, edges) -- nodes are 0..n-1, edges is a list of (u, v)
DIRECTED edges. Return True if the graph contains a directed cycle
(a self-loop counts), else False. The graph may be disconnected.

HOW TO WORK THROUGH THIS
-------------------------
DFS with three colours: 0 = unvisited, 1 = on the current path,
2 = finished. Reaching a node coloured 1 means a back edge, i.e. a cycle.
(Alternative: Kahn's algorithm -- if you cannot remove all nodes by
repeatedly taking in-degree 0, there is a cycle.)
Use an iterative DFS or Kahn's to avoid recursion limits on long chains.

Run: python3 cycle_detect_directed.py
"""


def has_cycle(n: int, edges: list) -> bool:
    raise NotImplementedError


def _run_tests():
    assert has_cycle(0, []) is False
    assert has_cycle(3, [(0, 1), (1, 2)]) is False
    assert has_cycle(3, [(0, 1), (1, 2), (2, 0)]) is True
    assert has_cycle(2, [(0, 0)]) is True
    assert has_cycle(4, [(0, 1), (0, 2), (1, 3), (2, 3)]) is False  # diamond
    assert has_cycle(5, [(0, 1), (3, 4), (4, 3)]) is True  # cycle in 2nd component
    long_chain = [(i, i + 1) for i in range(5000)]
    assert has_cycle(5001, long_chain) is False
    assert has_cycle(5001, long_chain + [(5000, 0)]) is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
