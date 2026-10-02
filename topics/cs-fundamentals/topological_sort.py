"""
Day 11, Task 8 -- CS fundamentals: topological sort (Kahn's algorithm).

THE PROBLEM
------------
deps is a dict: task -> list of tasks it DEPENDS ON (they must come
first). Tasks that appear only as dependencies count as nodes too.

Implement topo_order(deps) -> list that returns a valid ordering where
every task appears after all its dependencies. For determinism, when
several tasks are ready, pick the smallest (use a heap). Raise
ValueError("cycle") if the graph has a cycle.

HOW TO WORK THROUGH THIS
-------------------------
Compute in-degrees (number of unmet dependencies) and a reverse map
dep -> dependents. Start from in-degree 0 nodes; when you emit a node,
decrement its dependents. If you emitted fewer nodes than exist, there
is a cycle.

Run: python3 topological_sort.py
"""
import heapq  # noqa: F401


def topo_order(deps):
    nodes = set(deps)
    for ds in deps.values():
        nodes.update(ds)
    indeg = {n: 0 for n in nodes}
    dependents = {n: [] for n in nodes}
    for task, ds in deps.items():
        for d in set(ds):
            indeg[task] += 1
            dependents[d].append(task)
    heap = [n for n in nodes if indeg[n] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        n = heapq.heappop(heap)
        out.append(n)
        for m in dependents[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, m)
    if len(out) != len(nodes):
        raise ValueError("cycle")
    return out


def _run_tests() -> None:
    assert topo_order({}) == []
    assert topo_order({"a": []}) == ["a"]
    d = {"app": ["lib", "util"], "lib": ["core"], "util": ["core"], "core": []}
    assert topo_order(d) == ["core", "lib", "util", "app"]
    # nodes that only appear as dependencies
    assert topo_order({"b": ["a"]}) == ["a", "b"]
    # smallest-ready-first tiebreak
    assert topo_order({"c": [], "b": [], "a": []}) == ["a", "b", "c"]
    order = topo_order({"x": ["y"], "y": ["z"], "w": ["z"], "z": []})
    pos = {t: i for i, t in enumerate(order)}
    assert pos["z"] < pos["y"] < pos["x"] and pos["z"] < pos["w"]
    for cyc in ({"a": ["b"], "b": ["a"]}, {"a": ["a"]},
                {"a": ["b"], "b": ["c"], "c": ["a"], "d": []}):
        try:
            topo_order(cyc)
            assert False, "should detect cycle"
        except ValueError:
            pass
    print("All topological_sort tests passed.")


if __name__ == "__main__":
    _run_tests()
