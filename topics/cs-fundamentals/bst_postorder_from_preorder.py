"""
Day 50, Task 10 -- CS fundamentals: BST postorder from preorder.

THE PROBLEM
------------
pre is the preorder traversal of a binary search tree with distinct values.
bst_postorder_from_preorder(pre) returns the postorder traversal of that same tree
(empty list for empty input) WITHOUT assuming anything beyond the BST property.
Example: [8,5,1,7,10,12] -> [1,7,5,12,10,8].
Hint: the first element is the root; the first later value > root starts the right
subtree. Recurse (or use a stack / upper-bound index trick) and emit root last.

Run: python3 bst_postorder_from_preorder.py
"""


def bst_postorder_from_preorder(pre):
    raise NotImplementedError


def _run_tests():
    assert bst_postorder_from_preorder([8, 5, 1, 7, 10, 12]) == [1, 7, 5, 12, 10, 8]
    assert bst_postorder_from_preorder([]) == []
    assert bst_postorder_from_preorder([1]) == [1]
    assert bst_postorder_from_preorder([3, 2, 1]) == [1, 2, 3]
    assert bst_postorder_from_preorder([1, 2, 3]) == [3, 2, 1]
    assert bst_postorder_from_preorder([5, 3, 2, 4, 8, 7, 9]) == [2, 4, 3, 7, 9, 8, 5]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
