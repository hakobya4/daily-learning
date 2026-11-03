"""
Day 44, Task 1 -- Python: minimum domino rotations.

THE PROBLEM
------------
tops[i] and bottoms[i] are the two faces of domino i (values 1..6). One
rotation swaps the two faces of one domino. Return the minimum number of
rotations so that ALL values in tops are equal OR all values in bottoms are
equal. Return -1 if impossible.
Hint: only tops[0] or bottoms[0] can be the winning value; try both candidates
and count how many dominoes need a swap for each side.

Run: python3 minimum_domino_rotations.py
"""


def min_domino_rotations(tops, bottoms):
    raise NotImplementedError


def _run_tests():
    assert min_domino_rotations([2, 1, 2, 4, 2, 2], [5, 2, 6, 2, 3, 2]) == 2
    assert min_domino_rotations([3, 5, 1, 2, 3], [3, 6, 3, 3, 4]) == -1
    assert min_domino_rotations([1, 1, 1], [1, 1, 1]) == 0
    assert min_domino_rotations([1, 2], [2, 1]) == 1
    assert min_domino_rotations([1], [2]) == 0
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
