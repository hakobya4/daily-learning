"""
Day 4, Task 8 -- CS fundamentals: binary search tree.

THE PROBLEM
------------
Implement a BinarySearchTree class with:

  insert(value) -- inserts `value` maintaining BST ordering (values
                   less than a node go left, greater go right). If
                   `value` is already present anywhere in the tree,
                   insert() should be a no-op -- don't insert
                   duplicates.
  contains(value) -> bool -- True if `value` exists anywhere in the tree.
  inorder() -> list -- returns all values via an in-order traversal
                        (left, node, right), which for a BST comes out
                        in SORTED order -- that's the whole point of
                        this exercise.

An empty tree's inorder() is [] and contains() is False for anything.

HOW TO WORK THROUGH THIS
-------------------------
Build a small Node class first (value, left, right, all starting
None). For insert(): if the tree is empty, the new node becomes the
root; otherwise walk from the root, going left when value < node.value
and right when value > node.value, until you fall off the tree (a
None slot), and attach the new node there. Stop early (no-op) if you
hit a node whose value already equals the one being inserted.

For inorder(): recurse left, then record the current node's value,
then recurse right. Do this into an accumulator list rather than
trying to return partial lists and concatenate (simpler to get right).

Run: python3 binary_tree.py
"""


class _Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value) -> None:
        # TODO: if the tree is empty, `value` becomes the root.
        # Otherwise walk left/right by comparison until you find an
        # empty slot, and attach a new _Node there. No-op if a node
        # with this value already exists.
        raise NotImplementedError

    def contains(self, value) -> bool:
        # TODO: walk left/right by comparison starting at self.root;
        # return True if you land on a node with this value, False if
        # you fall off the tree.
        raise NotImplementedError

    def inorder(self) -> list:
        # TODO: in-order traversal (left, node, right) starting from
        # self.root, collecting values into a list as you go.
        raise NotImplementedError


def _run_tests() -> None:
    bst = BinarySearchTree()
    assert bst.inorder() == []
    assert bst.contains(5) is False

    for v in [5, 3, 8, 1, 4, 7, 9]:
        bst.insert(v)

    assert bst.inorder() == [1, 3, 4, 5, 7, 8, 9], bst.inorder()
    assert bst.contains(4) is True
    assert bst.contains(6) is False
    assert bst.contains(9) is True

    # duplicate insert should be a no-op
    bst.insert(5)
    assert bst.inorder() == [1, 3, 4, 5, 7, 8, 9], bst.inorder()

    print("All binary_tree tests passed.")


if __name__ == "__main__":
    _run_tests()
