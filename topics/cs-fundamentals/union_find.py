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
    def __init__(self, n: int):
        raise NotImplementedError

    def find(self, x: int) -> int:
        raise NotImplementedError

    def union(self, a: int, b: int) -> bool:
        raise NotImplementedError

    def connected(self, a: int, b: int) -> bool:
        raise NotImplementedError


def count_components(n: int, edges: list) -> int:
    raise NotImplementedError


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
