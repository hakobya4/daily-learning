"""
Day 36, Task 10 -- CS fundamentals: sorted array to height-balanced BST.

THE PROBLEM
------------
Given a strictly increasing list of ints, build a height-balanced binary
search tree (for every node, left/right subtree heights differ by <= 1)
and return its root (None for an empty list). Use the MIDDLE element as the
root (lower middle when the length is even), then recurse on each half.

Also implement:
  inorder(root)  -> list of values via in-order traversal
  height(root)   -> height in nodes (empty tree = 0)

  [1,2,3] -> root 2, left 1, right 3
  inorder(sorted_array_to_bst(xs)) == xs   for any sorted xs

Run: python3 sorted_array_to_bst.py
"""
from __future__ import annotations

from typing import Optional


class Node:
    def __init__(self, val: int, left: "Optional[Node]" = None, right: "Optional[Node]" = None):
        self.val = val
        self.left = left
        self.right = right


def sorted_array_to_bst(nums: list[int]) -> Optional[Node]:
    raise NotImplementedError


def inorder(root: Optional[Node]) -> list[int]:
    raise NotImplementedError


def height(root: Optional[Node]) -> int:
    raise NotImplementedError


def _is_balanced(root: Optional[Node]) -> bool:
    if root is None:
        return True
    return (
        abs(height(root.left) - height(root.right)) <= 1
        and _is_balanced(root.left)
        and _is_balanced(root.right)
    )


def _run_tests():
    assert sorted_array_to_bst([]) is None
    r = sorted_array_to_bst([1, 2, 3])
    assert (r.val, r.left.val, r.right.val) == (2, 1, 3)
    r = sorted_array_to_bst([5])
    assert r.val == 5 and r.left is None and r.right is None
    r = sorted_array_to_bst([1, 2])
    assert r.val == 1 and r.right.val == 2 and r.left is None
    for n in range(0, 40):
        xs = list(range(0, n * 3, 3))
        root = sorted_array_to_bst(xs)
        assert inorder(root) == xs
        assert _is_balanced(root)
    assert height(None) == 0
    assert height(sorted_array_to_bst(list(range(15)))) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
