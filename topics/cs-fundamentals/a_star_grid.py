"""
Day 56, Task 7 -- CS fundamentals: A* search on a weighted grid.

THE PROBLEM
------------
A grid is a list of equal-length strings. Each cell is one of:
  '#'        -- wall (impassable)
  '.'        -- open, cost 1 to ENTER
  '1'..'9'   -- open, cost equal to the digit to ENTER
  'S' / 'G'  -- start / goal (exactly one of each), cost 1 to enter

Moves are 4-directional (up/down/left/right). The cost of a path is the sum of the costs
of every cell ENTERED (the start cell is not paid for).

Implement:
  * shortest_path(grid) -> (cost, path) where path is the list of (row, col) from S to G
    inclusive, or (None, None) if G is unreachable. Any minimum-cost path is accepted.
  * astar_expansions(grid) -> how many nodes your A* popped-and-expanded (for curiosity;
    the test only checks that A* with the Manhattan heuristic expands NO MORE nodes than
    plain Dijkstra on an open grid -- implement dijkstra_expansions(grid) the same way
    with h = 0).

Rules:
  * Use the Manhattan distance |dr| + |dc| as the heuristic. Because every step costs
    >= 1 it is admissible AND consistent, so the first time you pop G its cost is optimal.
  * Missing S or G, more than one of either, or ragged rows -> ValueError.

Hint: heapq of (f = g + h, -g, (r, c)) -- on equal f, prefer the node with LARGER g (it is
closer to the goal), which matters a lot on open grids; keep best_g in a dict and skip stale heap entries
whose g is larger than best_g. Record parent[(r, c)] when you improve a neighbour, then walk
parents back from G to rebuild the path.

Run: python3 a_star_grid.py
"""


import heapq


def _parse(grid):
    if not grid or not grid[0]:
        raise ValueError("empty grid")
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("ragged rows")
    starts = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "S"]
    goals = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "G"]
    if len(starts) != 1 or len(goals) != 1:
        raise ValueError("need exactly one S and one G")
    return starts[0], goals[0]


def _search(grid, use_heuristic):
    start, goal = _parse(grid)
    rows, cols = len(grid), len(grid[0])
    gr, gc = goal

    def h(r, c):
        return abs(r - gr) + abs(c - gc) if use_heuristic else 0

    best_g = {start: 0}
    parent = {start: None}
    heap = [(h(*start), 0, start)]
    closed = set()
    expansions = 0
    while heap:
        f, neg_g, node = heapq.heappop(heap)
        g = -neg_g
        if node in closed or g > best_g.get(node, float("inf")):
            continue
        closed.add(node)
        expansions += 1
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return g, path[::-1], expansions
        r, c = node
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                ch = grid[nr][nc]
                if ch == "#":
                    continue
                ng = g + (int(ch) if ch.isdigit() else 1)
                if ng < best_g.get((nr, nc), float("inf")):
                    best_g[(nr, nc)] = ng
                    parent[(nr, nc)] = node
                    heapq.heappush(heap, (ng + h(nr, nc), -ng, (nr, nc)))
    return None, None, expansions


def shortest_path(grid):
    cost, path, _ = _search(grid, True)
    return cost, path


def astar_expansions(grid):
    return _search(grid, True)[2]


def dijkstra_expansions(grid):
    return _search(grid, False)[2]


def _path_cost(grid, path):
    total = 0
    for (r0, c0), (r1, c1) in zip(path, path[1:]):
        assert abs(r0 - r1) + abs(c0 - c1) == 1, "non-adjacent step"
        ch = grid[r1][c1]
        assert ch != "#", "walked through a wall"
        total += int(ch) if ch.isdigit() else 1
    return total


def _brute(grid):
    # Bellman-Ford style relaxation -- slow but obviously correct.
    rows, cols = len(grid), len(grid[0])
    INF = float("inf")
    dist = {}
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            if grid[r][c] == "G":
                goal = (r, c)
    dist[start] = 0
    changed = True
    while changed:
        changed = False
        for (r, c), d in list(dist.items()):
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                    ch = grid[nr][nc]
                    nd = d + (int(ch) if ch.isdigit() else 1)
                    if nd < dist.get((nr, nc), INF):
                        dist[(nr, nc)] = nd
                        changed = True
    return dist.get(goal)


def _run_tests():
    g1 = ["S..",
          ".#.",
          "..G"]
    cost, path = shortest_path(g1)
    assert cost == 4 and path[0] == (0, 0) and path[-1] == (2, 2) and len(path) == 5
    assert _path_cost(g1, path) == 4

    g2 = ["S9G",
          "111"]
    cost, path = shortest_path(g2)
    assert cost == 4, cost            # down, right, right, up -- cheaper than through 9
    assert _path_cost(g2, path) == 4

    g3 = ["S#G"]
    assert shortest_path(g3) == (None, None)

    g4 = ["SG"]
    assert shortest_path(g4) == (1, [(0, 0), (0, 1)])

    for bad in (["S.."], ["..G"], ["SSG"], ["S.G", ".."], ["SGG"]):
        try:
            shortest_path(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))

    import random
    rng = random.Random(56)
    for _ in range(150):
        rows, cols = rng.randint(1, 7), rng.randint(2, 7)
        cells = [[rng.choice("..#123459") for _ in range(cols)] for _ in range(rows)]
        sr, sc = rng.randrange(rows), rng.randrange(cols)
        while True:
            gr, gc = rng.randrange(rows), rng.randrange(cols)
            if (gr, gc) != (sr, sc):
                break
        cells[sr][sc] = "S"
        cells[gr][gc] = "G"
        grid = ["".join(row) for row in cells]
        exp = _brute(grid)
        cost, path = shortest_path(grid)
        assert cost == exp, (grid, cost, exp)
        if exp is not None:
            assert path[0] == (sr, sc) and path[-1] == (gr, gc)
            assert _path_cost(grid, path) == exp, grid

    # On an open grid the heuristic must pay off.
    open_grid = ["S" + "." * 59] + ["." * 60 for _ in range(58)] + ["." * 59 + "G"]
    cost, path = shortest_path(open_grid)
    assert cost == 118
    a, d = astar_expansions(open_grid), dijkstra_expansions(open_grid)
    assert 0 < a <= d, (a, d)

    big = ["S" + "." * 299] + ["." * 300 for _ in range(298)] + ["." * 299 + "G"]
    assert shortest_path(big)[0] == 598
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
