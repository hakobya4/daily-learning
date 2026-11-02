"""
Day 43, Task 10 -- CS fundamentals: strongly connected components (Tarjan).

THE PROBLEM
------------
scc(n, edges) -> list of components. Nodes are 0..n-1, edges is a list of
(u, v) directed pairs. Each component is a SORTED list of its nodes, and the
list of components is sorted too (so the result is deterministic), e.g.
  scc(5, [(0,1),(1,2),(2,0),(1,3),(3,4),(4,3)]) == [[0,1,2],[3,4]]
Use Tarjan's algorithm (index, lowlink, on-stack) or Kosaraju. A test uses a
3000-node cycle, so a naive recursive DFS will hit Python's recursion limit:
write the DFS iteratively (explicit stack) -- do not just raise the limit.

Run: python3 tarjan_scc.py
"""


def scc(n, edges):
    raise NotImplementedError


def _run_tests():
    assert scc(5, [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 3)]) == [[0, 1, 2], [3, 4]]
    assert scc(3, []) == [[0], [1], [2]]
    assert scc(4, [(0, 1), (1, 2), (2, 3)]) == [[0], [1], [2], [3]]
    assert scc(2, [(0, 0), (0, 1)]) == [[0], [1]]
    assert scc(0, []) == []
    assert scc(4, [(0, 1), (1, 0), (2, 3), (3, 2)]) == [[0, 1], [2, 3]]
    big = [(i, (i + 1) % 3000) for i in range(3000)]
    assert scc(3000, big) == [list(range(3000))]
    chain = [(i, i + 1) for i in range(2999)]
    res = scc(3000, chain)
    assert len(res) == 3000 and res[0] == [0] and res[-1] == [2999]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
