"""
Day 53, Task 3 -- CS fundamentals: eventual safe states (cycle detection in a directed graph).

THE PROBLEM
------------
eventual_safe_nodes(graph): graph[i] is the list of nodes that node i has a directed edge to.
A TERMINAL node has no outgoing edges. A node is SAFE if every path starting from it ends at
a terminal node (i.e. no path from it can reach a cycle). Return all safe nodes in ascending
order.
Example: [[1, 2], [2, 3], [5], [0], [5], [], []] -> [2, 4, 5, 6]
(0 -> 1 -> 3 -> 0 is a cycle, so 0, 1, 3 are unsafe).
Hint (pick one): three-colour DFS (white / grey = on stack / black = safe), or reverse every
edge and run Kahn's algorithm from the terminal nodes -- whatever gets peeled is safe.
A self-loop makes a node unsafe. O(V + E).

Run: python3 eventual_safe_states.py
"""


def eventual_safe_nodes(graph):
    raise NotImplementedError


def _run_tests():
    assert eventual_safe_nodes([]) == []
    assert eventual_safe_nodes([[]]) == [0]
    assert eventual_safe_nodes([[0]]) == []
    assert eventual_safe_nodes([[1], [2], []]) == [0, 1, 2]
    assert eventual_safe_nodes([[1, 2], [2, 3], [5], [0], [5], [], []]) == [2, 4, 5, 6]
    assert eventual_safe_nodes([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]) == [4]
    assert eventual_safe_nodes([[1], [0], [3], []]) == [2, 3]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
