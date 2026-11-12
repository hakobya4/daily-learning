"""
Day 52, Task 3 -- CS fundamentals: multi-source reverse BFS/DFS (Pacific Atlantic water flow).

THE PROBLEM
------------
pacific_atlantic(heights): heights is an m x n grid of cell heights. The Pacific ocean touches
the top and left edges, the Atlantic the bottom and right edges. Rain water flows from a cell
to a 4-directional neighbour whose height is LESS THAN OR EQUAL to the current one, and from
any edge cell into the ocean(s) it touches. Return a sorted list of [row, col] for every cell
from which water can reach BOTH oceans.
Hint: don't search from every cell. Start one BFS/DFS from all Pacific edge cells and one from
all Atlantic edge cells, walking "uphill" (to neighbours >= current), and intersect the two
reachable sets. O(m * n).

Run: python3 pacific_atlantic_flow.py
"""


def pacific_atlantic(heights):
    if not heights or not heights[0]:
        return []
    m, n = len(heights), len(heights[0])

    def reach(starts):
        seen = set(starts)
        stack = list(starts)
        while stack:
            r, c = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]):
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return seen

    pacific = reach([(0, c) for c in range(n)] + [(r, 0) for r in range(m)])
    atlantic = reach([(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m)])
    return sorted([r, c] for r, c in pacific & atlantic)


def _run_tests():
    grid = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4],
    ]
    assert pacific_atlantic(grid) == [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    assert pacific_atlantic([[1]]) == [[0, 0]]
    assert pacific_atlantic([]) == []
    assert pacific_atlantic([[2, 1], [1, 2]]) == [[0, 0], [0, 1], [1, 0], [1, 1]]
    assert pacific_atlantic([[3, 3, 3], [3, 1, 3], [3, 3, 3]]) == [
        [0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]
    ]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
