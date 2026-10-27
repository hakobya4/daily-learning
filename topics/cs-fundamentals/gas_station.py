"""
Day 37, Task 9 -- CS fundamentals: gas station circuit (greedy).

THE PROBLEM
------------
There are n stations on a circular route. gas[i] is the fuel available at
station i; cost[i] is the fuel needed to drive from station i to i+1
(wrapping around). The tank starts empty. Return the index of the station
from which you can complete one full clockwise lap, or -1 if impossible.
If a solution exists it is guaranteed unique.

  gas=[1,2,3,4,5], cost=[3,4,5,1,2] -> 3
  gas=[2,3,4],     cost=[3,4,3]     -> -1

HOW TO WORK THROUGH THIS
-------------------------
If sum(gas) < sum(cost) the answer is -1. Otherwise scan once keeping a
running tank; whenever it goes negative at station i, no start in
(start..i) can work, so reset start = i + 1 and tank = 0. O(n), O(1).

Run: python3 gas_station.py
"""


def can_complete_circuit(gas: list, cost: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert can_complete_circuit([2, 3, 4], [3, 4, 3]) == -1
    assert can_complete_circuit([5], [4]) == 0
    assert can_complete_circuit([4], [5]) == -1
    assert can_complete_circuit([5, 1, 2, 3, 4], [4, 4, 1, 5, 1]) == 4
    assert can_complete_circuit([3, 1, 1], [1, 2, 2]) == 0
    assert can_complete_circuit([2, 0, 0, 5], [1, 1, 1, 1]) == 3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
