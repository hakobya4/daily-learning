"""
Day 22, Task 4 -- Python: car fleets.

THE PROBLEM
------------
Cars drive toward a target on a one-lane road. car i starts at
position[i] (all distinct) with constant speed speed[i]. A car cannot pass
the one in front: it catches up and then drives at that car's speed,
forming a FLEET (cars that arrive together count as one fleet).

Return the number of fleets that arrive at the target.

  car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3
  car_fleet(10, [3], [3]) == 1
  car_fleet(100, [0, 2, 4], [4, 2, 1]) == 1

Raise ValueError if the two lists differ in length.

HOW TO WORK THROUGH THIS
-------------------------
Sort cars by position descending; compute each car's time to target
(target - pos) / speed. Walk from the front: a car starts a NEW fleet only
if its time is strictly greater than the current fleet leader's time.
(Use exact comparison via cross-multiplication or fractions if you like.)

Run: python3 car_fleet.py
"""


def car_fleet(target: int, position: list, speed: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3
    assert car_fleet(10, [3], [3]) == 1
    assert car_fleet(100, [0, 2, 4], [4, 2, 1]) == 1
    assert car_fleet(10, [], []) == 0
    assert car_fleet(10, [0, 4], [1, 1]) == 2
    assert car_fleet(10, [6, 0], [1, 10]) == 1
    assert car_fleet(10, [0, 5], [5, 2]) == 1
    try:
        car_fleet(10, [1, 2], [1])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
