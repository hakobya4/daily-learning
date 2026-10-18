"""
Day 28, Task 2 -- Python: daily temperatures (monotonic stack).

THE PROBLEM
------------
daily_temperatures(temps) returns a list where answer[i] is the number of
days you must wait after day i for a warmer temperature. If there is no
warmer day in the future, answer[i] is 0.

  daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) -> [1, 1, 4, 2, 1, 1, 0, 0]
  daily_temperatures([30, 40, 50, 60])                  -> [1, 1, 1, 0]
  daily_temperatures([])                                -> []

HOW TO WORK THROUGH THIS
-------------------------
Keep a stack of indices whose answer is still unknown (temperatures
decreasing). When a warmer day arrives, pop and fill in the distances.
Target O(n).

Run: python3 daily_temperatures.py
"""


def daily_temperatures(temps: list) -> list:
    raise NotImplementedError


def _run_tests():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert daily_temperatures([60, 50, 40, 30]) == [0, 0, 0, 0]
    assert daily_temperatures([]) == []
    assert daily_temperatures([50]) == [0]
    assert daily_temperatures([50, 50, 50]) == [0, 0, 0]
    assert daily_temperatures([70, 60, 80, 65, 90]) == [2, 1, 2, 1, 0]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
