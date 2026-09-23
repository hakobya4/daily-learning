"""
Day 3, Task 2 -- Python: flatten an arbitrarily nested list.

THE PROBLEM
------------
Write flatten(nested) that takes a list which may contain integers
and/or other lists (nested to any depth) and returns a single flat
list of integers, in the original left-to-right order.

Example: flatten([1, [2, [3, 4], 5], 6]) -> [1, 2, 3, 4, 5, 6]

This is a recursion warm-up: the base case is "this element is an
int, keep it"; the recursive case is "this element is a list, flatten
IT and extend the result with whatever comes back."

HOW TO WORK THROUGH THIS
-------------------------
Write it recursively first. If you finish early, try a second,
iterative version using an explicit stack instead of recursion.

Run: python3 flatten_nested_list.py
"""


def flatten(nested: list) -> list:
    result = []
    for element in nested:
        if isinstance(element, list):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result


def flatten_iterative(nested: list) -> list:
    """Second version: explicit stack instead of recursion."""
    result = []
    stack = list(reversed(nested))
    while stack:
        element = stack.pop()
        if isinstance(element, list):
            stack.extend(reversed(element))
        else:
            result.append(element)
    return result


def _run_tests() -> None:
    cases = [
        ([], []),
        ([1, 2, 3], [1, 2, 3]),
        ([1, [2, [3, 4], 5], 6], [1, 2, 3, 4, 5, 6]),
        ([[1, [2]], [[3]], 4], [1, 2, 3, 4]),
        ([[]], []),
    ]
    for nested, expected in cases:
        got = flatten(nested)
        assert got == expected, f"flatten({nested!r}) -> {got!r}, expected {expected!r}"
        got_iter = flatten_iterative(nested)
        assert got_iter == expected, (
            f"flatten_iterative({nested!r}) -> {got_iter!r}, expected {expected!r}"
        )
    print("All flatten_nested_list tests passed.")


if __name__ == "__main__":
    _run_tests()
