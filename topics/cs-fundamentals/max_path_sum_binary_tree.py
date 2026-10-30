"""
Day 39, Task 9 -- CS fundamentals: binary tree maximum path sum.

THE PROBLEM
------------
A path is any sequence of nodes connected by parent-child edges, visiting
each node at most once; it need not pass through the root. Return the
maximum sum of node values over all non-empty paths. Values may be negative.

  [-10, 9, 20, None, None, 15, 7]  -> 42   (15 -> 20 -> 7)
  [1, 2, 3]                        -> 6
  [-3]                             -> -3

HOW TO WORK THROUGH THIS
-------------------------
Post-order DFS. For each node compute the best "downward" gain it can
offer its parent: node.val + max(0, left_gain, right_gain)... but a path
bending at this node may use BOTH children: val + max(0,left) + max(0,right).
Update a global best with the bending value, return the one-sided gain.
O(n) time, O(h) space.

Run: python3 max_path_sum_binary_tree.py
"""
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(level_order):
    """Build a tree from a LeetCode-style level-order list (None = missing)."""
    if not level_order or level_order[0] is None:
        return None
    root = TreeNode(level_order[0])
    q = deque([root])
    i = 1
    while q and i < len(level_order):
        node = q.popleft()
        if i < len(level_order) and level_order[i] is not None:
            node.left = TreeNode(level_order[i])
            q.append(node.left)
        i += 1
        if i < len(level_order) and level_order[i] is not None:
            node.right = TreeNode(level_order[i])
            q.append(node.right)
        i += 1
    return root


def max_path_sum(root) -> int:
    best = float("-inf")

    def gain(node):
        nonlocal best
        if node is None:
            return 0
        left = max(0, gain(node.left))
        right = max(0, gain(node.right))
        best = max(best, node.val + left + right)
        return node.val + max(left, right)

    gain(root)
    return best


def _run_tests():
    assert max_path_sum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42
    assert max_path_sum(build_tree([1, 2, 3])) == 6
    assert max_path_sum(build_tree([-3])) == -3
    assert max_path_sum(build_tree([2, -1])) == 2
    assert max_path_sum(build_tree([-2, -1])) == -1
    assert max_path_sum(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])) == 48
    assert max_path_sum(build_tree([1, -2, 3])) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
