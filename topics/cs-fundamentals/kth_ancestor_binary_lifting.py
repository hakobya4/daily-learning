"""
Day 48, Task 9 -- CS fundamentals: k-th ancestor of a tree node (binary lifting).

THE PROBLEM
------------
A tree has n nodes 0..n-1; parent[i] is the parent of i and parent[0] == -1 (root).
Implement class TreeAncestor(n, parent) with get_kth_ancestor(node, k) returning the
k-th ancestor of node, or -1 if it does not exist. k = 0 returns node itself.
Preprocess in O(n log n) with up[j][v] = the 2**j-th ancestor of v, then answer each
query in O(log k) by walking the set bits of k.

Run: python3 kth_ancestor_binary_lifting.py
"""


class TreeAncestor:
    def __init__(self, n, parent):
        self.LOG = max(1, n.bit_length())
        self.up = [list(parent)]
        for j in range(1, self.LOG):
            prev = self.up[j - 1]
            self.up.append([-1 if prev[v] == -1 else prev[prev[v]] for v in range(n)])

    def get_kth_ancestor(self, node, k):
        if k >= (1 << self.LOG):
            return -1
        for j in range(self.LOG):
            if k >> j & 1:
                node = self.up[j][node]
                if node == -1:
                    return -1
        return node


def _run_tests():
    t = TreeAncestor(7, [-1, 0, 0, 1, 1, 2, 2])
    assert t.get_kth_ancestor(3, 1) == 1
    assert t.get_kth_ancestor(5, 2) == 0
    assert t.get_kth_ancestor(6, 3) == -1
    assert t.get_kth_ancestor(4, 0) == 4
    assert t.get_kth_ancestor(0, 1) == -1
    n = 1000
    chain = TreeAncestor(n, [-1] + list(range(n - 1)))
    assert chain.get_kth_ancestor(n - 1, n - 1) == 0
    assert chain.get_kth_ancestor(n - 1, n) == -1
    assert chain.get_kth_ancestor(500, 123) == 377
    assert chain.get_kth_ancestor(7, 10 ** 9) == -1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
