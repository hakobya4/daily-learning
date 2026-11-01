"""
Day 42, Task 10 -- CS fundamentals: cheapest path with at most K stops.

THE PROBLEM
------------
cheapest_price(n, flights, src, dst, k) -> minimum total price to go from
city src to city dst using at most k stops (k intermediate cities, so at most
k+1 flights). flights is a list of (from, to, price) directed edges over
cities 0..n-1. Return -1 if impossible.
Hint: Bellman-Ford limited to k+1 rounds, using a copy of the distance array
each round (so one round extends paths by exactly one edge).

Run: python3 cheapest_flights.py
"""


def cheapest_price(n, flights, src, dst, k):
    raise NotImplementedError


def _run_tests():
    f = [(0, 1, 100), (1, 2, 100), (0, 2, 500)]
    assert cheapest_price(3, f, 0, 2, 1) == 200
    assert cheapest_price(3, f, 0, 2, 0) == 500
    assert cheapest_price(3, f, 2, 0, 5) == -1
    assert cheapest_price(3, f, 1, 1, 0) == 0
    g = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 3, 10)]
    assert cheapest_price(4, g, 0, 3, 0) == 10
    assert cheapest_price(4, g, 0, 3, 1) == 10
    assert cheapest_price(4, g, 0, 3, 2) == 3
    h = [(0, 1, 5), (1, 2, 5), (0, 2, 20), (2, 1, 1)]
    assert cheapest_price(3, h, 0, 1, 3) == 5
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
