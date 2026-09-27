"""
Day 6, Task 8 -- CS fundamentals: min-heap from scratch.

THE PROBLEM
------------
Implement a MinHeap class backed by a plain Python list, with:

  push(value) -> None     -- add a value, maintaining the heap property.
  pop() -> value           -- remove and return the SMALLEST value.
  peek() -> value          -- return (without removing) the smallest value.
  __len__(self) -> int     -- number of elements currently in the heap.

Do NOT use Python's built-in `heapq` module -- the point of this
exercise is implementing sift-up/sift-down yourself over an array,
which is what heapq does internally.

A binary min-heap stored in a list has this shape: for a node at index
i, its children are at indices 2*i+1 and 2*i+2, and its parent is at
(i-1)//2. The heap property: every node's value is <= both its
children's values (this is what makes the root, index 0, always the
minimum).

HOW TO WORK THROUGH THIS
-------------------------
push: append the new value at the END of the list, then "sift up" --
while it's smaller than its parent, swap it with its parent and
repeat, until it's not smaller than its parent or it reaches the root.

pop: save the root (index 0) to return later. Move the LAST element in
the list to index 0, remove the old last slot, then "sift down" from
the root -- while it's bigger than the SMALLER of its two children,
swap with that smaller child, and repeat, until it is smaller than
both remaining children or it has no children left.

Handle the edge cases: popping from an empty heap, and a heap with
just one element (sifting is a no-op either way).

Run: python3 min_heap.py
"""


class MinHeap:
    def __init__(self):
        self._data = []

    def __len__(self) -> int:
        return len(self._data)

    def peek(self):
        return self._data[0]

    def push(self, value) -> None:
        self._data.append(value)
        i = len(self._data) - 1
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i] < self._data[parent]:
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break

    def pop(self):
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            i = 0
            n = len(self._data)
            while True:
                left = 2 * i + 1
                right = 2 * i + 2
                smallest = i
                if left < n and self._data[left] < self._data[smallest]:
                    smallest = left
                if right < n and self._data[right] < self._data[smallest]:
                    smallest = right
                if smallest == i:
                    break
                self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
                i = smallest
        return top


def _run_tests() -> None:
    h = MinHeap()
    assert len(h) == 0

    for v in [5, 3, 8, 1, 9, 2, 7]:
        h.push(v)

    assert len(h) == 7
    assert h.peek() == 1

    popped = [h.pop() for _ in range(7)]
    assert popped == sorted([5, 3, 8, 1, 9, 2, 7]), popped
    assert len(h) == 0

    # single element
    h2 = MinHeap()
    h2.push(42)
    assert h2.peek() == 42
    assert h2.pop() == 42
    assert len(h2) == 0

    print("All min_heap tests passed.")


if __name__ == "__main__":
    _run_tests()
