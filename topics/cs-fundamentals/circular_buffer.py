"""
Day 22, Task 10 -- CS fundamentals: fixed-capacity circular buffer.

THE PROBLEM
------------
Implement class CircularBuffer(capacity) backed by a fixed-size list and
two indices (no collections.deque, no list.pop(0)):

  push(x)    append x; if full, OVERWRITE the oldest item
  pop()      remove and return the oldest item; IndexError if empty
  peek()     return the oldest item without removing; IndexError if empty
  len(buf)   number of items currently stored
  to_list()  items oldest -> newest
  is_full()  True when len == capacity

Raise ValueError if capacity < 1. All operations are O(1) except to_list.

  b = CircularBuffer(3); b.push(1); b.push(2); b.push(3); b.push(4)
  b.to_list() == [2, 3, 4]; b.pop() == 2

HOW TO WORK THROUGH THIS
-------------------------
Keep _data, _head (index of oldest), _size. Write index is
(_head + _size) % capacity; when full, advance _head instead of growing.

Run: python3 circular_buffer.py
"""


class CircularBuffer:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._cap = capacity
        self._data = [None] * capacity
        self._head = 0
        self._size = 0

    def push(self, x):
        if self._size == self._cap:
            self._data[self._head] = x
            self._head = (self._head + 1) % self._cap
        else:
            self._data[(self._head + self._size) % self._cap] = x
            self._size += 1

    def pop(self):
        if self._size == 0:
            raise IndexError("pop from empty buffer")
        x = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._cap
        self._size -= 1
        return x

    def peek(self):
        if self._size == 0:
            raise IndexError("peek at empty buffer")
        return self._data[self._head]

    def __len__(self):
        return self._size

    def to_list(self) -> list:
        return [self._data[(self._head + i) % self._cap] for i in range(self._size)]

    def is_full(self) -> bool:
        return self._size == self._cap


def _run_tests():
    try:
        CircularBuffer(0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    b = CircularBuffer(3)
    assert len(b) == 0 and not b.is_full() and b.to_list() == []
    for f in (b.pop, b.peek):
        try:
            f()
        except IndexError:
            pass
        else:
            raise AssertionError("expected IndexError")
    b.push(1); b.push(2)
    assert b.to_list() == [1, 2] and len(b) == 2 and not b.is_full()
    b.push(3)
    assert b.is_full() and b.peek() == 1
    b.push(4)
    assert b.to_list() == [2, 3, 4] and len(b) == 3
    assert b.pop() == 2 and b.to_list() == [3, 4]
    b.push(5); b.push(6)
    assert b.to_list() == [4, 5, 6]
    assert [b.pop(), b.pop(), b.pop()] == [4, 5, 6]
    assert len(b) == 0
    one = CircularBuffer(1)
    one.push("a"); one.push("b")
    assert one.to_list() == ["b"] and one.pop() == "b"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
