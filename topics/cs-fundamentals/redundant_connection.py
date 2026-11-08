"""
Day 49, Task 10 -- CS fundamentals: redundant connection (union-find on edges).

THE PROBLEM
------------
A tree with n nodes labelled 1..n had one extra edge added, creating exactly one cycle.
find_redundant(edges) takes the list of [u, v] edges (n edges for n nodes) and returns the
edge that can be removed so the result is a tree again. If several edges qualify, return the
one that appears LAST in the input.
Examples: [[1,2],[1,3],[2,3]] -> [2,3];
[[1,2],[2,3],[3,4],[1,4],[1,5]] -> [1,4].
Hint: process edges in order with union-find (path compression); the first edge whose
endpoints already share a root closes the cycle and is the answer.

Run: python3 redundant_connection.py
"""


def find_redundant(edges):
    raise NotImplementedError


def _run_tests():
    assert find_redundant([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert find_redundant([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    assert find_redundant([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]) == [1, 3]
    assert find_redundant([[1, 2], [2, 3], [1, 3]]) == [1, 3]
    assert find_redundant([[2, 7], [7, 8], [3, 6], [2, 5], [6, 8], [4, 8], [2, 8], [1, 8], [7, 10], [3, 9]]) == [2, 8]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
