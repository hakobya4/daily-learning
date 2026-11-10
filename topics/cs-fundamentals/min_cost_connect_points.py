"""
Day 51, Task 10 -- CS fundamentals: minimum spanning tree over points.

THE PROBLEM
------------
min_cost_connect_points(points): points is a list of [x, y]. The cost of connecting two
points is their Manhattan distance |x1-x2| + |y1-y2|. Return the minimum total cost to
connect ALL points so that every pair is reachable (i.e. the weight of a minimum spanning tree).
Examples: [[0,0],[2,2],[3,10],[5,2],[7,0]] -> 20, [[3,12],[-2,5],[-4,1]] -> 18.
Hint: Prim's algorithm in O(n^2) with a "best known distance" array (no heap needed for a
dense graph), or Kruskal over all pairs with union-find.

Run: python3 min_cost_connect_points.py
"""


def min_cost_connect_points(points):
    raise NotImplementedError


def _run_tests():
    assert min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
    assert min_cost_connect_points([[3, 12], [-2, 5], [-4, 1]]) == 18
    assert min_cost_connect_points([[0, 0]]) == 0
    assert min_cost_connect_points([[0, 0], [1, 1]]) == 2
    assert min_cost_connect_points([[0, 0], [0, 0], [0, 0]]) == 0
    assert min_cost_connect_points([[0, 0], [1, 0], [2, 0], [3, 0]]) == 3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
