"""
Day 32, Task 10 -- CS fundamentals: lowest common ancestor of a binary tree.

THE PROBLEM
------------
A binary tree is given as nested tuples (value, left, right) with None for
a missing child. All values are unique. lca(tree, a, b) returns the value
of the lowest node that has both a and b in its subtree (a node counts as
a descendant of itself). If either value is missing from the tree return
None.

  tree = (3, (5, (6,None,None), (2, (7,None,None), (4,None,None))),
             (1, (0,None,None), (8,None,None)))
  lca(tree, 5, 1) -> 3
  lca(tree, 5, 4) -> 5
  lca(tree, 7, 4) -> 2
  lca(tree, 7, 99) -> None

HOW TO WORK THROUGH THIS
-------------------------
Post-order recursion returning (found_a, found_b, answer). If both sides
report a hit, the current node is the answer. Remember to verify BOTH
values exist before trusting a "found" result.

Run: python3 lowest_common_ancestor.py
"""


def lca(tree, a, b):
    raise NotImplementedError


def _run_tests():
    L = lambda v: (v, None, None)
    tree = (3, (5, L(6), (2, L(7), L(4))), (1, L(0), L(8)))
    assert lca(tree, 5, 1) == 3
    assert lca(tree, 5, 4) == 5
    assert lca(tree, 7, 4) == 2
    assert lca(tree, 6, 4) == 5
    assert lca(tree, 0, 8) == 1
    assert lca(tree, 3, 8) == 3
    assert lca(tree, 7, 7) == 7
    assert lca(tree, 7, 99) is None
    assert lca(None, 1, 2) is None
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
