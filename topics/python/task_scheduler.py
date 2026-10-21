"""
Day 31, Task 4 -- Python: task scheduler (least intervals).

THE PROBLEM
------------
tasks is a string where each letter is a task that takes one time unit.
Between two runs of the SAME task there must be at least n idle-or-other
units (a cooldown of n). Tasks can run in any order. least_interval(tasks, n)
returns the minimum total number of time units needed (idle units count).

  ("AAABBB", 2) -> 8    A B _ A B _ A B
  ("AAABBB", 0) -> 6
  ("A", 5)      -> 1

HOW TO WORK THROUGH THIS
-------------------------
Greedy / counting: let m = highest frequency and k = how many tasks have
that frequency. The frame is (m-1)*(n+1) + k. If there are more tasks than
the frame can hold there is no idle time at all, so the answer is
max(len(tasks), frame).

Run: python3 task_scheduler.py
"""


def least_interval(tasks: str, n: int) -> int:
    raise NotImplementedError


def _run_tests():
    assert least_interval("AAABBB", 2) == 8
    assert least_interval("AAABBB", 0) == 6
    assert least_interval("AAAAAABCDEFG", 2) == 16
    assert least_interval("A", 5) == 1
    assert least_interval("", 3) == 0
    assert least_interval("ABCD", 10) == 4
    assert least_interval("AABB", 1) == 4
    assert least_interval("AAAB", 2) == 7
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
