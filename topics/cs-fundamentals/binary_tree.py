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
        if self.root is None:
            self.root = _Node(value)
            return
        node = self.root
        while True:
            if value == node.value:
                return
            elif value < node.value:
                if node.left is None:
                    node.left = _Node(value)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = _Node(value)
                    return
                node = node.right

    def contains(self, value) -> bool:
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def inorder(self) -> list:
        result: list = []

        def _walk(node):
            if node is None:
                return
            _walk(node.left)
            result.append(node.value)
            _walk(node.right)

        _walk(self.root)
        return result


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
