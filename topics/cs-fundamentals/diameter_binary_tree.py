"""
Day 37, Task 10 -- CS fundamentals: diameter of a binary tree.

THE PROBLEM
------------
The diameter of a binary tree is the number of EDGES on the longest path
between any two nodes (the path need not pass through the root).
Implement diameter(root); an empty tree (None) has diameter 0, a single
node has diameter 0.

        1
       / \
      2   3        diameter = 3  (4-2-1-3 or 5-2-1-3)
     / \
    4   5

HOW TO WORK THROUGH THIS
-------------------------
Post-order DFS returning the height of each subtree (height of None = 0
nodes, or -1 in edges -- pick one and be consistent). At each node the
best path THROUGH it is left_height + right_height; keep a running max
(nonlocal variable or a one-element list). O(n).

Run: python3 diameter_binary_tree.py
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def diameter(root) -> int:
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        lh = height(node.left)
        rh = height(node.right)
        best = max(best, lh + rh)
        return 1 + max(lh, rh)

    height(root)
    return best


def _run_tests():
    N = TreeNode
    assert diameter(None) == 0
    assert diameter(N(1)) == 0
    assert diameter(N(1, N(2))) == 1
    t = N(1, N(2, N(4), N(5)), N(3))
    assert diameter(t) == 3
    # longest path does not pass through the root
    left = N(2, N(3, N(4, N(5)), None), N(6, None, N(7, None, N(8))))
    root = N(1, left, N(9))
    assert diameter(root) == 6
    # skewed chain of 6 nodes
    chain = N(1)
    cur = chain
    for v in range(2, 7):
        cur.right = N(v)
        cur = cur.right
    assert diameter(chain) == 5
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
