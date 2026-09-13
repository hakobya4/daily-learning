"""
Day 2, Task 7 -- Python: CSV summary statistics.

THE PROBLEM
------------
Write summarize(rows, column) that takes a list of dict rows (as you'd
get from csv.DictReader) and a column name, and returns a dict with
that column's min, max, and mean as floats -- e.g.
{"min": 1.0, "max": 9.0, "mean": 5.0}.

This practices two things at once: using the standard `csv` module
correctly (DictReader, and that every value comes back as a STRING --
you have to convert it yourself), and doing a simple aggregation pass
without reaching for a library like pandas for something this small.

HOW TO WORK THROUGH THIS
-------------------------
1. Create a small sample.csv yourself (a few rows, one numeric column
   plus whatever else you want, e.g. name,score).
2. Load it with csv.DictReader in a small script or the REPL, print
   what a row actually looks like (it's a dict of strings) before
   writing summarize().
3. Implement summarize() below against that shape.

Run: python3 csv_stats.py
"""

import csv
import io


def summarize(rows: list[dict], column: str) -> dict:
    # TODO: extract `column` from each row, cast to float, and compute
    # min/max/mean. Raise ValueError if `rows` is empty.
    raise NotImplementedError


def _run_tests() -> None:
    sample_csv = "name,score\nAlice,10\nBob,20\nCarol,30\n"
    rows = list(csv.DictReader(io.StringIO(sample_csv)))

    result = summarize(rows, "score")
    assert result == {"min": 10.0, "max": 30.0, "mean": 20.0}, result

    try:
        summarize([], "score")
        assert False, "expected ValueError on empty rows"
    except ValueError:
        pass

    print("All csv_stats tests passed.")


if __name__ == "__main__":
    _run_tests()
