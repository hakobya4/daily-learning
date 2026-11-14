"""
Day 54, Task 3 -- CS fundamentals: minimum height trees (topological leaf trimming).

THE PROBLEM
------------
An undirected TREE has n nodes labelled 0..n-1 and n-1 edges. Choosing any node as the root
gives a rooted tree with some height (edges on the longest root-to-leaf path). Return the
SORTED list of all roots that give the minimum possible height. There are always 1 or 2.

Example: n = 6, edges [(3,0),(3,1),(3,2),(3,4),(5,4)] -> [3, 4]
         n = 4, edges [(1,0),(1,2),(1,3)]             -> [1]

Running BFS from every node is O(n^2). Aim for O(n).
Hint: the answer is the centre of the tree's longest path. Peel the tree like an onion:
put all current leaves (degree 1) in a queue, remove them layer by layer (decrementing
neighbours' degrees and enqueuing new leaves) until 1 or 2 nodes remain -- those are the
answer. Special case: n == 1 -> [0].
Raise ValueError if n < 1 or len(edges) != n - 1.

Run: python3 minimum_height_trees.py
"""


def find_min_height_trees(n, edges):
    if n < 1 or len(edges) != n - 1:
        raise ValueError("expected a tree with n >= 1 nodes and n - 1 edges")
    if n == 1:
        return [0]
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    degree = [len(nb) for nb in adj]
    leaves = [i for i in range(n) if degree[i] == 1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)
        nxt = []
        for leaf in leaves:
            for v in adj[leaf]:
                degree[v] -= 1
                if degree[v] == 1:
                    nxt.append(v)
        leaves = nxt
    return sorted(leaves)


def _height_from(n, edges, root):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = {root}
    frontier = [root]
    h = -1
    while frontier:
        h += 1
        nxt = []
        for u in frontier:
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    nxt.append(v)
        frontier = nxt
    return h


def _brute(n, edges):
    hs = [_height_from(n, edges, r) for r in range(n)]
    best = min(hs)
    return [r for r in range(n) if hs[r] == best]


def _run_tests():
    assert find_min_height_trees(6, [(3, 0), (3, 1), (3, 2), (3, 4), (5, 4)]) == [3, 4]
    assert find_min_height_trees(4, [(1, 0), (1, 2), (1, 3)]) == [1]
    assert find_min_height_trees(1, []) == [0]
    assert find_min_height_trees(2, [(0, 1)]) == [0, 1]
    assert find_min_height_trees(3, [(0, 1), (1, 2)]) == [1]
    # A path of 7 nodes 0-1-2-3-4-5-6: centre is 3.
    assert find_min_height_trees(7, [(i, i + 1) for i in range(6)]) == [3]
    # A path of 8 nodes: two centres.
    assert find_min_height_trees(8, [(i, i + 1) for i in range(7)]) == [3, 4]

    import random
    rng = random.Random(54)
    for _ in range(200):
        n = rng.randint(1, 25)
        edges = [(rng.randrange(i), i) for i in range(1, n)]   # random tree
        labels = list(range(n))
        rng.shuffle(labels)
        edges = [(labels[a], labels[b]) for a, b in edges]
        assert find_min_height_trees(n, edges) == _brute(n, edges), (n, edges)

    # Large path must be fast (O(n)).
    n = 200_000
    assert find_min_height_trees(n, [(i, i + 1) for i in range(n - 1)]) == [99_999, 100_000]

    for bad in [(0, []), (3, [(0, 1)])]:
        try:
            find_min_height_trees(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
