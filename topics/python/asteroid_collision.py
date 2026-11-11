"""
Day 52, Task 1 -- Python: asteroid collision (stack simulation).

THE PROBLEM
------------
asteroid_collision(asteroids): each integer is an asteroid moving along a line; the absolute
value is its size and the sign its direction (positive = right, negative = left). All move at
the same speed. When a right-mover meets a left-mover, the smaller one explodes; if both are
the same size, both explode. Two asteroids moving in the same direction never meet.
Return the list of asteroids left after all collisions, in order.
Examples: [5, 10, -5] -> [5, 10], [8, -8] -> [], [10, 2, -5] -> [10], [-2, -1, 1, 2] -> [-2, -1, 1, 2].
Hint: scan left to right with a stack; only a negative asteroid can hit the stack's top, and
only if that top is positive. One asteroid may destroy several in a row.

Run: python3 asteroid_collision.py
"""


def asteroid_collision(asteroids):
    raise NotImplementedError


def _run_tests():
    assert asteroid_collision([]) == []
    assert asteroid_collision([5, 10, -5]) == [5, 10]
    assert asteroid_collision([8, -8]) == []
    assert asteroid_collision([10, 2, -5]) == [10]
    assert asteroid_collision([-2, -1, 1, 2]) == [-2, -1, 1, 2]
    assert asteroid_collision([1, -2, -2, -2]) == [-2, -2, -2]
    assert asteroid_collision([1, 2, 3, -10, 4]) == [-10, 4]
    assert asteroid_collision([3, 5, -5, -3]) == []
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
