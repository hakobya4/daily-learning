"""
Day 38, Task 10 -- CS fundamentals: reverse a linked list in groups of k.

THE PROBLEM
------------
Given the head of a singly linked list and an integer k >= 1, reverse the
nodes k at a time and return the new head. If fewer than k nodes remain at
the end, leave them as they are. Relink nodes -- do not just swap values.

  1->2->3->4->5, k=2 -> 2->1->4->3->5
  1->2->3->4->5, k=3 -> 3->2->1->4->5

HOW TO WORK THROUGH THIS
-------------------------
Use a dummy node before head. For each group: first check that k nodes
exist (walk ahead), then reverse exactly those k nodes with the usual
prev/cur pointer flip, and stitch the group's old first node (now its
tail) to the start of the next group. O(n) time, O(1) extra space.

Run: python3 reverse_k_group.py
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def from_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse_k_group(head, k: int):
    raise NotImplementedError


def _run_tests():
    assert to_list(reverse_k_group(from_list([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert to_list(reverse_k_group(from_list([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
    assert to_list(reverse_k_group(from_list([1, 2, 3, 4, 5]), 1)) == [1, 2, 3, 4, 5]
    assert to_list(reverse_k_group(from_list([1, 2, 3, 4]), 4)) == [4, 3, 2, 1]
    assert to_list(reverse_k_group(from_list([1, 2, 3]), 5)) == [1, 2, 3]
    assert to_list(reverse_k_group(None, 2)) is not None
    assert to_list(reverse_k_group(None, 2)) == []
    # relinking, not value swapping: node identities move
    head = from_list([1, 2, 3, 4])
    first = head
    new_head = reverse_k_group(head, 2)
    assert new_head.val == 2 and new_head.next is first
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
