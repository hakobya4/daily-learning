"""
Day 11, Task 7 -- CS fundamentals: Dijkstra's shortest paths.

THE PROBLEM
------------
Graph is a dict: node -> list of (neighbour, weight) with weight >= 0.
Implement:

  shortest_distances(graph, source) -> dict[node, float]
      Distance from source to every node reachable from it
      (unreachable nodes are simply absent). Use a heap (heapq).

  shortest_path(graph, source, target) -> list | None
      The actual node list from source to target, or None if
      unreachable. source == target returns [source].

Raise ValueError if any edge weight is negative.

HOW TO WORK THROUGH THIS
-------------------------
Push (dist, node) onto a heap; skip stale entries when popped dist is
greater than the best known. Track a `prev` map for path rebuilding.

Run: python3 dijkstra.py
"""
import heapq  # noqa: F401


def shortest_distances(graph, source):
    raise NotImplementedError


def shortest_path(graph, source, target):
    raise NotImplementedError


def _run_tests() -> None:
    g = {
        "A": [("B", 7), ("C", 9), ("F", 14)],
        "B": [("A", 7), ("C", 10), ("D", 15)],
        "C": [("A", 9), ("B", 10), ("D", 11), ("F", 2)],
        "D": [("B", 15), ("C", 11), ("E", 6)],
        "E": [("D", 6), ("F", 9)],
        "F": [("A", 14), ("C", 2), ("E", 9)],
        "Z": [],
    }
    d = shortest_distances(g, "A")
    assert d == {"A": 0, "B": 7, "C": 9, "D": 20, "E": 20, "F": 11}, d
    assert "Z" not in d
    assert shortest_path(g, "A", "E") == ["A", "C", "F", "E"]
    assert shortest_path(g, "A", "A") == ["A"]
    assert shortest_path(g, "A", "Z") is None
    # zero-weight edges and a directed graph
    h = {1: [(2, 0), (3, 5)], 2: [(3, 1)], 3: []}
    assert shortest_distances(h, 1) == {1: 0, 2: 0, 3: 1}
    assert shortest_path(h, 3, 1) is None
    try:
        shortest_distances({1: [(2, -1)], 2: []}, 1)
        assert False, "should reject negative weight"
    except ValueError:
        pass
    print("All dijkstra tests passed.")


if __name__ == "__main__":
    _run_tests()
