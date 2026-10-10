"""
Day 19, Task 10 -- CS fundamentals: a stack with O(1) get_min.

THE PROBLEM
------------
Implement MinStack with push(x), pop(), top(), get_min() -- all O(1).
pop(), top() and get_min() raise IndexError on an empty stack.
pop() returns the removed value. len(stack) returns the size.

HOW TO WORK THROUGH THIS
-------------------------
Keep a second stack of running minimums (or store (value, min_so_far)
pairs). Mind duplicates of the minimum when popping.

Run: python3 min_stack.py
"""


class MinStack:
    def __init__(self):
        self._items = []  # (value, min_so_far)

    def push(self, x):
        m = x if not self._items else min(x, self._items[-1][1])
        self._items.append((x, m))

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()[0]

    def top(self):
        if not self._items:
            raise IndexError("top of empty stack")
        return self._items[-1][0]

    def get_min(self):
        if not self._items:
            raise IndexError("get_min of empty stack")
        return self._items[-1][1]

    def __len__(self):
        return len(self._items)


def _run_tests():
    s = MinStack()
    assert len(s) == 0
    s.push(5)
    s.push(3)
    s.push(3)
    s.push(8)
    assert s.top() == 8 and s.get_min() == 3 and len(s) == 4
    assert s.pop() == 8
    assert s.pop() == 3
    assert s.get_min() == 3
    assert s.pop() == 3
    assert s.get_min() == 5
    s.push(-1)
    assert s.get_min() == -1
    s.pop()
    assert s.get_min() == 5 and s.top() == 5
    s.pop()
    for op in (s.pop, s.top, s.get_min):
        try:
            op()
        except IndexError:
            pass
        else:
            raise AssertionError("expected IndexError on empty stack")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
