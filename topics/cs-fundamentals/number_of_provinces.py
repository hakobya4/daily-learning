"""
Day 50, Task 4 -- CS fundamentals: number of provinces (connected components).

THE PROBLEM
------------
is_connected is an n x n symmetric 0/1 matrix; is_connected[i][j] == 1 means city i and
city j are directly connected (and is_connected[i][i] == 1). A province is a group of
cities connected directly or indirectly. count_provinces(is_connected) returns the number
of provinces (0 for an empty matrix).
Hint: DFS/BFS over the adjacency matrix, or union-find with a component counter.

Run: python3 number_of_provinces.py
"""


def count_provinces(is_connected):
    n = len(is_connected)
    seen = [False] * n
    count = 0
    for start in range(n):
        if seen[start]:
            continue
        count += 1
        stack = [start]
        seen[start] = True
        while stack:
            u = stack.pop()
            for v in range(n):
                if is_connected[u][v] and not seen[v]:
                    seen[v] = True
                    stack.append(v)
    return count


def _run_tests():
    assert count_provinces([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert count_provinces([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    assert count_provinces([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 1
    assert count_provinces([]) == 0
    assert count_provinces([[1]]) == 1
    assert count_provinces([[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1]]) == 2
    assert count_provinces([[1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 1]]) == 2
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
