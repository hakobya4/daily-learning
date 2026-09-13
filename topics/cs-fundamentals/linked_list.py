"""
Day 2, Task 6 -- CS fundamentals: singly linked list from scratch.

THE PROBLEM
------------
Implement a bare-bones singly linked list with:
  - append(value)         -- add to the end, O(n) unless you track a tail
  - prepend(value)         -- add to the front, O(1)
  - find(value) -> bool    -- True if value exists anywhere in the list
  - to_list() -> list      -- return contents as a plain Python list, in order

The point isn't that Python needs this (it has real lists) -- it's
understanding what a list library gives you "for free" (indexing,
O(1) append) that a linked structure does NOT get for free, and why
you'd still choose a linked list in other languages/contexts (O(1)
insertion at an arbitrary known node, no need to shift elements).

HOW TO WORK THROUGH THIS
-------------------------
Build the Node class first (holds a value and a `next` pointer), then
the LinkedList class that chains Nodes together via self.head.

Run: python3 linked_list.py
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value) -> None:
        # TODO: if empty, new node becomes head; otherwise walk to the
        # last node and attach the new node after it.
        raise NotImplementedError

    def prepend(self, value) -> None:
        # TODO: new node's `next` points at the current head, then it
        # becomes the new head.
        raise NotImplementedError

    def find(self, value) -> bool:
        # TODO: walk the chain from head, return True if any node matches.
        raise NotImplementedError

    def to_list(self) -> list:
        # TODO: walk the chain from head, collecting values in order.
        raise NotImplementedError


def _run_tests() -> None:
    ll = LinkedList()
    assert ll.to_list() == []
    assert ll.find(1) is False

    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3], ll.to_list()

    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2, 3], ll.to_list()

    assert ll.find(2) is True
    assert ll.find(99) is False

    print("All linked list tests passed.")


if __name__ == "__main__":
    _run_tests()
