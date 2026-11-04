"""
Day 44, Task 10 -- CS fundamentals: egg drop.

THE PROBLEM
------------
egg_drop(eggs, floors) returns the minimum number of drops needed, in the
WORST case, to find the highest floor from which an egg survives, given
`eggs` identical eggs and a building with `floors` floors. A broken egg is
gone; a surviving egg can be reused.
Hint: flip the DP -- f[t][e] = max floors you can resolve with t drops and e
eggs = f[t-1][e-1] + f[t-1][e] + 1. Find the smallest t with f[t][eggs] >= floors.

Run: python3 egg_drop.py
"""


def egg_drop(eggs, floors):
    if floors <= 0:
        return 0
    f = [0] * (eggs + 1)
    t = 0
    while f[eggs] < floors:
        t += 1
        for e in range(eggs, 0, -1):
            f[e] = f[e - 1] + f[e] + 1
    return t


def _run_tests():
    assert egg_drop(1, 2) == 2
    assert egg_drop(2, 6) == 3
    assert egg_drop(3, 14) == 4
    assert egg_drop(2, 100) == 14
    assert egg_drop(1, 10) == 10
    assert egg_drop(2, 36) == 8
    assert egg_drop(5, 0) == 0
    assert egg_drop(10, 1) == 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
