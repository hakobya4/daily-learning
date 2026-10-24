"""
Day 34, Task 4 -- Python: exclusive time of functions.

THE PROBLEM
------------
A single-threaded CPU runs n functions with ids 0..n-1. logs is a list of
strings "id:start:ts" or "id:end:ts" (ts is an integer time unit; a
function that starts at ts is running during unit ts, and one that ends at
ts is still running during unit ts, so it covers ts - start + 1 units).
Functions can call each other (a stack). Return a list of length n with
each function's EXCLUSIVE time: time spent in it, not in functions it
called.

  n=2, ["0:start:0","1:start:2","1:end:5","0:end:6"]  -> [3, 4]
  n=1, ["0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"]
                                                      -> [8]

HOW TO WORK THROUGH THIS
-------------------------
Keep a stack of running ids and the time `prev` of the last event. On
"start": credit ts - prev to the function on top of the stack (if any),
push, prev = ts. On "end": credit ts - prev + 1 to the top, pop, and set
prev = ts + 1.

Run: python3 exclusive_time.py
"""


def exclusive_time(n: int, logs: list) -> list:
    raise NotImplementedError


def _run_tests():
    assert exclusive_time(2, ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]) == [3, 4]
    assert exclusive_time(
        1, ["0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7"]
    ) == [8]
    assert exclusive_time(
        2, ["0:start:0", "0:start:2", "0:end:5", "1:start:6", "1:end:6", "0:end:7"]
    ) == [7, 1]
    assert exclusive_time(1, ["0:start:0", "0:end:0"]) == [1]
    assert exclusive_time(3, []) == [0, 0, 0]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
