"""
Day 40, Task 1 -- Python: lemonade stand change.

THE PROBLEM
------------
Lemonade costs 5. Customers queue and each pays with a bill of 5, 10 or 20
(bills list, in order). You start with no money. Each customer buys one
lemonade and you must give correct change immediately using bills you have
received so far. Return True if you can serve everybody, else False.

  can_give_change([5, 5, 5, 10, 20]) -> True
  can_give_change([5, 5, 10, 10, 20]) -> False

HOW TO WORK THROUGH THIS
-------------------------
Track counts of 5s and 10s only (20s are never used as change). For a 20,
prefer giving 10+5 over 5+5+5 -- greedy works because 5s are more flexible.

Run: python3 lemonade_change.py
"""


def can_give_change(bills: list) -> bool:
    raise NotImplementedError


def _run_tests():
    assert can_give_change([5, 5, 5, 10, 20]) is True
    assert can_give_change([5, 5, 10, 10, 20]) is False
    assert can_give_change([]) is True
    assert can_give_change([10]) is False
    assert can_give_change([5, 10, 5, 20]) is True
    assert can_give_change([5, 5, 5, 20]) is True
    assert can_give_change([5, 20]) is False
    assert can_give_change([5, 5, 10, 20, 20]) is False
    assert can_give_change([5] * 10 + [10] * 5 + [20] * 2) is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
