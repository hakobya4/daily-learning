"""
Day 35, Task 9 -- CS fundamentals: clone an undirected graph (DFS/BFS + hash map).

THE PROBLEM
------------
Nodes have a value and a list of neighbours. Given a reference to one node
of a connected undirected graph, return a DEEP COPY: every node is a new
object (no node shared with the original) but the structure and values are
identical. Return None for None. Cycles must be handled.

HOW TO WORK THROUGH THIS
-------------------------
Keep a dict old_node -> new_node. When you first see a node, create its
copy and store it BEFORE recursing into neighbours (that breaks cycles).
Then for each neighbour, clone it (or reuse the stored copy) and append.

Run: python3 clone_graph.py
"""


class Node:
    def __init__(self, val, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node):
    raise NotImplementedError


def _build(adj):
    """adj: dict val -> list of neighbour vals (1-indexed style). Returns node 1 (or None)."""
    if not adj:
        return None
    nodes = {v: Node(v) for v in adj}
    for v, ns in adj.items():
        nodes[v].neighbors = [nodes[n] for n in ns]
    return nodes[min(adj)]


def _collect(start):
    seen, stack, out = {}, [start], {}
    while stack:
        n = stack.pop()
        if id(n) in seen:
            continue
        seen[id(n)] = n
        out[n.val] = sorted(x.val for x in n.neighbors)
        stack.extend(n.neighbors)
    return out, list(seen.values())


def _run_tests():
    assert clone_graph(None) is None

    single = Node(1)
    c = clone_graph(single)
    assert c is not single and c.val == 1 and c.neighbors == []

    adj = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}
    g = _build(adj)
    c = clone_graph(g)
    orig_struct, orig_nodes = _collect(g)
    new_struct, new_nodes = _collect(c)
    assert new_struct == orig_struct == {k: sorted(v) for k, v in adj.items()}
    assert {id(n) for n in orig_nodes}.isdisjoint({id(n) for n in new_nodes})
    assert len(new_nodes) == 4

    # self-contained cycle with a triangle
    adj = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    g = _build(adj)
    c = clone_graph(g)
    assert _collect(c)[0] == {k: sorted(v) for k, v in adj.items()}
    assert c is not g
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
