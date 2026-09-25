"""
Day 5, Task 8 -- CS fundamentals: graph traversal (BFS and DFS).

THE PROBLEM
------------
Represent a graph as an adjacency list: a dict mapping each node to a
list of its neighbors, e.g. {"A": ["B", "C"], "B": ["D"], ...}. Write:

  bfs(graph, start) -> list -- breadth-first traversal order starting
                               from `start`, visiting each node once.
  dfs(graph, start) -> list -- depth-first traversal order starting
                               from `start`, visiting each node once.

For both, when a node has multiple unvisited neighbors, visit them in
the order they appear in that node's adjacency list.

HOW TO WORK THROUGH THIS
-------------------------
BFS: use a queue (collections.deque) and a `visited` set. Enqueue
`start` and mark it visited immediately; then repeatedly pop from the
LEFT, record the popped node, and enqueue any of its unvisited
neighbors -- marking each visited the MOMENT it's enqueued, not when
it's later popped, otherwise the same node can get enqueued twice.

DFS: the recursive version is simplest -- visit the current node
(record it, mark it visited), then recurse into each of its neighbors,
in order, skipping any that are already visited.

Run: python3 graph_bfs_dfs.py
"""

from collections import deque


def bfs(graph: dict, start: str) -> list:
    # TODO: queue-based breadth-first traversal. Mark a node visited
    # at ENQUEUE time, not at pop time.
    raise NotImplementedError


def dfs(graph: dict, start: str) -> list:
    # TODO: recursive (or explicit-stack) depth-first traversal.
    raise NotImplementedError


def _run_tests() -> None:
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    assert bfs(graph, "A") == ["A", "B", "C", "D", "E", "F"], bfs(graph, "A")
    assert dfs(graph, "A") == ["A", "B", "D", "E", "F", "C"], dfs(graph, "A")

    # single-node graph with no edges
    assert bfs({"X": []}, "X") == ["X"]
    assert dfs({"X": []}, "X") == ["X"]

    print("All graph_bfs_dfs tests passed.")


if __name__ == "__main__":
    _run_tests()
