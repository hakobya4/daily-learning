"""
Day 10, Task 7 -- CS fundamentals: validate a binary search tree.

THE PROBLEM
------------
Given the root of a binary tree of ints, return True iff it is a valid
BST: for every node, ALL values in its left subtree are strictly less
than the node's value and ALL values in its right subtree are strictly
greater (no duplicates allowed). An empty tree (None) is valid.

Beware the classic bug: checking only node.left.val < node.val <
node.right.val is NOT enough (see the last test).

HOW TO WORK THROUGH THIS
-------------------------
Pass (low, high) bounds down the recursion, or do an in-order traversal
and check the values are strictly increasing. State the time and space
complexity in a comment when you are done.

Run: python3 bst_validate.py
"""


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root) -> bool:
    # Pass (low, high) exclusive bounds down. Time O(n), space O(h) recursion.
    def check(node, low, high):
        if node is None:
            return True
        if (low is not None and node.val <= low) or (high is not None and node.val >= high):
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)

    return check(root, None, None)


def _run_tests() -> None:
    assert is_valid_bst(None) is True
    assert is_valid_bst(Node(1)) is True
    assert is_valid_bst(Node(2, Node(1), Node(3))) is True
    assert is_valid_bst(Node(2, Node(2), Node(3))) is False   # duplicate
    assert is_valid_bst(Node(5, Node(1), Node(4, Node(3), Node(6)))) is False
    #      5
    #     / \
    #    4   6
    #       / \
    #      3   7      <- 3 is < 5 but sits in the right subtree
    tricky = Node(5, Node(4), Node(6, Node(3), Node(7)))
    assert is_valid_bst(tricky) is False
    big = Node(10, Node(5, Node(2), Node(7)), Node(15, Node(12), Node(20)))
    assert is_valid_bst(big) is True
    print("All bst_validate tests passed.")


if __name__ == "__main__":
    _run_tests()
