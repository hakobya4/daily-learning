"""
Day 56, Task 2 -- Python: minimum number of refueling stops (greedy with a max-heap).

THE PROBLEM
------------
A car drives east from position 0 towards a target `target` miles away. It starts with
`start_fuel` liters, burns 1 liter per mile, and has an UNLIMITED tank. `stations` is a
list of [position, fuel] pairs sorted by position ascending (0 < position < target):
when the car is at a station it may stop and take ALL of that station's fuel.

Return the minimum number of stops needed to reach target, or -1 if it is impossible.
Arriving anywhere (a station or the target) with exactly 0 fuel left is fine.

Also implement which_stops(target, start_fuel, stations): one optimal list of station
INDICES (ascending) that achieves the minimum, or None if impossible. Any optimal set is
accepted; the tests verify it by simulation, not by exact value.

Example:
  min_refuel_stops(1, 1, [])                                         -> 0
  min_refuel_stops(100, 1, [[10, 100]])                              -> -1
  min_refuel_stops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]) -> 2
      (stop at 10 -> fuel 60 after paying 10 miles, reach 60 with 10 left, stop -> 50,
       finish with 10 to spare)

Hint: drive as far as the current fuel allows, pushing every station you PASS onto a
max-heap of fuel amounts (heapq with negated values). Only when you cannot reach the next
station (or the target) do you "retroactively" stop at the biggest station you passed --
pop from the heap. If the heap is empty at that moment, it is impossible. This gives
O(n log n). (The O(n^2) DP "dp[k] = farthest reach with k stops" is a nice second
solution to check against.)

Run: python3 min_refueling_stops.py
"""


def min_refuel_stops(target, start_fuel, stations):
    raise NotImplementedError


def which_stops(target, start_fuel, stations):
    raise NotImplementedError


def _simulate(target, start_fuel, stations, chosen):
    fuel, pos = start_fuel, 0
    chosen = set(chosen)
    for i, (p, f) in enumerate(stations):
        fuel -= p - pos
        pos = p
        if fuel < 0:
            return False
        if i in chosen:
            fuel += f
    return fuel - (target - pos) >= 0


def _dp(target, start_fuel, stations):
    dp = [start_fuel] + [0] * len(stations)
    for i, (p, f) in enumerate(stations):
        for k in range(i, -1, -1):
            if dp[k] >= p:
                dp[k + 1] = max(dp[k + 1], dp[k] + f)
    for k, reach in enumerate(dp):
        if reach >= target:
            return k
    return -1


def _run_tests():
    assert min_refuel_stops(1, 1, []) == 0
    assert min_refuel_stops(100, 1, [[10, 100]]) == -1
    assert min_refuel_stops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]) == 2
    assert min_refuel_stops(100, 50, [[25, 25], [50, 50]]) == 1
    assert min_refuel_stops(100, 25, [[25, 25], [50, 25], [75, 25]]) == 3
    assert min_refuel_stops(10, 5, [[5, 4]]) == -1
    assert min_refuel_stops(10, 5, [[5, 5]]) == 1

    assert which_stops(100, 1, [[10, 100]]) is None
    st = [[10, 60], [20, 30], [30, 30], [60, 40]]
    ws = which_stops(100, 10, st)
    assert len(ws) == 2 and ws == sorted(ws) and _simulate(100, 10, st, ws)
    assert which_stops(1, 1, []) == []

    import random
    rng = random.Random(56)
    for _ in range(400):
        target = rng.randint(1, 60)
        positions = sorted(rng.sample(range(1, target), min(rng.randint(0, 8), target - 1))) \
            if target > 1 else []
        stations = [[p, rng.randint(1, 20)] for p in positions]
        start = rng.randint(1, 25)
        exp = _dp(target, start, stations)
        assert min_refuel_stops(target, start, stations) == exp, (target, start, stations)
        ws = which_stops(target, start, stations)
        if exp == -1:
            assert ws is None
        else:
            assert len(ws) == exp and ws == sorted(ws), (target, start, stations, ws)
            assert _simulate(target, start, stations, ws), (target, start, stations, ws)

    # O(n log n): 200k stations, each just reachable from the previous one.
    n = 200_000
    big = [[i, 1] for i in range(1, n + 1)]
    assert min_refuel_stops(n + 1, 1, big) == n
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
