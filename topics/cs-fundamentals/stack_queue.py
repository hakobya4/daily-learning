"""
Day 3, Task 7 -- CS fundamentals: stack and queue from a plain list.

THE PROBLEM
------------
Implement two small classes backed by a plain Python list:

  Stack (LIFO):
    push(value)    -- add to the top
    pop() -> value  -- remove and return the top; raise IndexError if empty
    peek() -> value -- return the top without removing it; raise IndexError if empty
    is_empty() -> bool

  Queue (FIFO):
    enqueue(value)     -- add to the back
    dequeue() -> value -- remove and return the front; raise IndexError if empty
    is_empty() -> bool

The point: a Python list is a fine stack as-is (append/pop from the
end are both O(1)), but naive list.pop(0) for a queue is O(n) since
everything shifts -- collections.deque is the real answer for a queue,
but build it on a plain list first so you FEEL why deque exists.

Run: python3 stack_queue.py
"""


class Stack:
    def __init__(self):
        self._items = []

    def push(self, value) -> None:
        self._items.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0


class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, value) -> None:
        self._items.append(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def is_empty(self) -> bool:
        return len(self._items) == 0


def _run_tests() -> None:
    s = Stack()
    assert s.is_empty() is True
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.peek() == 3
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.is_empty() is False
    assert s.pop() == 1
    assert s.is_empty() is True
    try:
        s.pop()
        assert False, "expected IndexError on pop from empty stack"
    except IndexError:
        pass

    q = Queue()
    assert q.is_empty() is True
    q.enqueue("a")
    q.enqueue("b")
    q.enqueue("c")
    assert q.dequeue() == "a"
    assert q.dequeue() == "b"
    assert q.is_empty() is False
    assert q.dequeue() == "c"
    assert q.is_empty() is True
    try:
        q.dequeue()
        assert False, "expected IndexError on dequeue from empty queue"
    except IndexError:
        pass

    print("All stack_queue tests passed.")


if __name__ == "__main__":
    _run_tests()
