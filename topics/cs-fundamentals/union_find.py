"""
Day 10, Task 8 -- CS fundamentals: union-find (disjoint set union).

THE PROBLEM
------------
Implement class UnionFind for elements 0..n-1:

  UnionFind(n)
  find(x)        -> representative of x's set (use path compression)
  union(a, b)    -> merge the sets of a and b (union by size or rank);
                    return True if they were separate, False if already
                    in the same set
  connected(a,b) -> bool
  count          -> attribute: current number of disjoint sets

Then use it in count_components(n, edges) -> number of connected
components of an undirected graph with n nodes and the given edge list.

HOW TO WORK THROUGH THIS
-------------------------
parent[i] = i initially. find() walks up to the root and re-points nodes
along the way. Note the near-O(1) amortised cost in a comment.

Run: python3 union_find.py
"""


class UnionFind:
    # Path compression + union by size: amortised near-O(1) (inverse Ackermann).
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # iterative compression, no recursion limit
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)


def count_components(n: int, edges: list) -> int:
    uf = UnionFind(n)
    for a, b in edges:
        uf.union(a, b)
    return uf.count


def _run_tests() -> None:
    uf = UnionFind(5)
    assert uf.count == 5
    assert uf.union(0, 1) is True
    assert uf.union(1, 0) is False
    assert uf.union(3, 4) is True
    assert uf.count == 3
    assert uf.connected(0, 1) and not uf.connected(0, 3)
    uf.union(1, 4)
    assert uf.connected(0, 3) and uf.count == 2
    assert uf.find(0) == uf.find(4)

    assert count_components(5, [(0, 1), (1, 2), (3, 4)]) == 2
    assert count_components(4, []) == 4
    assert count_components(3, [(0, 1), (1, 2), (0, 2)]) == 1
    big = UnionFind(100000)
    for i in range(99999):
        big.union(i, i + 1)   # deep chain: must not blow the recursion limit
    assert big.count == 1 and big.connected(0, 99999)
    print("All union_find tests passed.")


if __name__ == "__main__":
    _run_tests()
