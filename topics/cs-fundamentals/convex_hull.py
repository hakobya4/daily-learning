"""
Day 58, Task 7 -- CS fundamentals: convex hull (Andrew's monotone chain) + area + point location.

THE PROBLEM
------------
Points are (x, y) tuples of INTEGERS. Use exact integer arithmetic only (no floats,
no atan2): everything is built on the cross product
    cross(o, a, b) = (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
which is > 0 for a counter-clockwise turn o->a->b, < 0 clockwise, 0 collinear.

Implement:

  convex_hull(points) -> list of points
      The hull vertices in COUNTER-CLOCKWISE order, starting at the lowest-x point
      (ties: lowest y). Duplicate points and points lying on a hull edge (collinear)
      are NOT included. Degenerate inputs: [] -> []; all points equal -> [that point];
      all collinear -> [the two extreme points] (lowest-x/lowest-y one first).

  twice_area(polygon) -> int
      Twice the signed area by the shoelace formula (positive for CCW order).
      Fewer than 3 vertices -> 0.

  locate(hull, p) -> "inside" | "boundary" | "outside"
      Where p lies relative to a hull returned by convex_hull (any size, including
      the degenerate 0/1/2-vertex hulls: a 2-vertex hull is a segment, so points on
      it are "boundary"). Must run in O(log n) for hulls with >= 3 vertices: binary-
      search the fan of triangles (hull[0], hull[i], hull[i+1]).

Example:
  pts = [(0, 0), (2, 0), (4, 0), (4, 4), (0, 4), (2, 2), (1, 3), (0, 2), (0, 0)]
  convex_hull(pts)                 -> [(0, 0), (4, 0), (4, 4), (0, 4)]
  twice_area([(0,0),(4,0),(4,4),(0,4)]) -> 32
  locate(hull, (2, 2)) -> "inside";  locate(hull, (4, 1)) -> "boundary";
  locate(hull, (5, 1)) -> "outside"

Hint: sort the unique points; build the lower chain left->right popping while the last
two points and the new one do NOT make a strict left turn (cross <= 0 pops collinear
points too); build the upper chain right->left the same way; concatenate, dropping the
last point of each chain (it repeats the first point of the other).

Run: python3 convex_hull.py
"""


def convex_hull(points):
    pts = sorted(set(tuple(p) for p in points))
    if len(pts) <= 1:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def twice_area(polygon):
    n = len(polygon)
    if n < 3:
        return 0
    total = 0
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        total += x1 * y2 - x2 * y1
    return total


def _on_segment(a, b, p):
    return (_cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def locate(hull, p):
    p = tuple(p)
    n = len(hull)
    if n == 0:
        return "outside"
    if n == 1:
        return "boundary" if p == tuple(hull[0]) else "outside"
    if n == 2:
        return "boundary" if _on_segment(hull[0], hull[1], p) else "outside"
    o = hull[0]
    c1 = _cross(o, hull[1], p)
    c2 = _cross(o, hull[-1], p)
    if c1 < 0 or c2 > 0:
        return "outside"                 # outside the wedge at hull[0]
    if c1 == 0:
        return "boundary" if _on_segment(o, hull[1], p) else "outside"
    if c2 == 0:
        return "boundary" if _on_segment(o, hull[-1], p) else "outside"
    # binary search the fan: largest i in [1, n-2] with p left of (or on) o->hull[i]
    lo, hi = 1, n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _cross(o, hull[mid], p) >= 0:
            lo = mid
        else:
            hi = mid
    c = _cross(hull[lo], hull[lo + 1], p)
    if c > 0:
        return "inside"
    if c == 0:
        return "boundary"
    return "outside"


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _brute_hull_set(points):
    # a point is a hull vertex iff some line through it has all other points strictly
    # on one side or on the line but "behind" it -- here: brute via all pairs.
    pts = sorted(set(points))
    if len(pts) <= 1:
        return set(pts)
    verts = set()
    for a in pts:
        for b in pts:
            if a == b:
                continue
            side = [_cross(a, b, c) for c in pts]
            if all(s >= 0 for s in side):
                # a-b is a supporting line; its extreme points on the line are vertices
                on = [c for c, s in zip(pts, side) if s == 0]
                verts.add(min(on))
                verts.add(max(on))
    return verts


def _brute_locate(points, p):
    pts = sorted(set(points))
    if not pts:
        return "outside"
    if len(pts) == 1:
        return "boundary" if p == pts[0] else "outside"
    sides = []
    on_any = False
    hull_set = _brute_hull_set(points)
    for a in pts:
        for b in pts:
            if a == b:
                continue
            side = [_cross(a, b, c) for c in pts]
            if all(s >= 0 for s in side):
                c = _cross(a, b, p)
                if c < 0:
                    return "outside"
                if c == 0:
                    on_line = [q for q, s in zip(pts, side) if s == 0]
                    lo, hi = min(on_line), max(on_line)
                    if lo <= p <= hi:
                        on_any = True
                    else:
                        return "outside"
                sides.append(c)
    if len(hull_set) == 2:   # segment
        return "boundary" if on_any else "outside"
    return "boundary" if on_any else "inside"


def _run_tests():
    pts = [(0, 0), (2, 0), (4, 0), (4, 4), (0, 4), (2, 2), (1, 3), (0, 2), (0, 0)]
    hull = convex_hull(pts)
    assert hull == [(0, 0), (4, 0), (4, 4), (0, 4)]
    assert twice_area(hull) == 32
    assert twice_area(list(reversed(hull))) == -32
    assert locate(hull, (2, 2)) == "inside"
    assert locate(hull, (4, 1)) == "boundary"
    assert locate(hull, (0, 0)) == "boundary"
    assert locate(hull, (5, 1)) == "outside"
    assert locate(hull, (2, -1)) == "outside"

    assert convex_hull([]) == []
    assert convex_hull([(3, 3), (3, 3)]) == [(3, 3)]
    assert convex_hull([(2, 2), (0, 0), (1, 1), (3, 3)]) == [(0, 0), (3, 3)]
    assert convex_hull([(0, 5), (0, 1), (0, 3)]) == [(0, 1), (0, 5)]
    assert convex_hull([(0, 0), (1, 1), (2, 0), (1, -1)]) == [(0, 0), (1, -1), (2, 0), (1, 1)]
    assert convex_hull([(0, 2), (0, 0), (2, 1)]) == [(0, 0), (2, 1), (0, 2)]
    assert twice_area([(0, 0), (1, 1)]) == 0
    assert twice_area([(0, 0), (2, 1), (0, 2)]) == 4

    assert locate([], (0, 0)) == "outside"
    assert locate([(1, 1)], (1, 1)) == "boundary"
    assert locate([(1, 1)], (1, 2)) == "outside"
    seg = [(0, 0), (4, 2)]
    assert locate(seg, (2, 1)) == "boundary"
    assert locate(seg, (6, 3)) == "outside"
    assert locate(seg, (1, 1)) == "outside"

    import random
    rng = random.Random(58)
    for _ in range(400):
        n = rng.randint(1, 12)
        pts = [(rng.randint(-4, 4), rng.randint(-4, 4)) for _ in range(n)]
        hull = convex_hull(pts)
        assert set(hull) == _brute_hull_set(pts), pts
        assert len(hull) == len(set(hull))
        if hull:
            assert hull[0] == min(hull)
        if len(hull) >= 3:
            m = len(hull)
            assert all(_cross(hull[i], hull[(i + 1) % m], hull[(i + 2) % m]) > 0
                       for i in range(m)), hull
            assert twice_area(hull) > 0
        for _ in range(5):
            q = (rng.randint(-5, 5), rng.randint(-5, 5))
            assert locate(hull, q) == _brute_locate(pts, q), (pts, hull, q)

    import time
    big = [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(100_000)]
    t0 = time.time()
    hull = convex_hull(big)
    queries = [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(100_000)]
    res = [locate(hull, q) for q in queries]
    assert res.count("inside") > 90_000
    assert time.time() - t0 < 10, "too slow -- O(n log n) hull, O(log n) locate"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
