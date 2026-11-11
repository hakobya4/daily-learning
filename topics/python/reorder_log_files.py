"""
Day 51, Task 3 -- Python: reorder log files.

THE PROBLEM
------------
reorder_logs(logs): each log is "<identifier> <content>". If the first token of the content
is a digit-only word the log is a DIGIT-log, otherwise a LETTER-log.
Return the logs reordered so that:
  - all letter-logs come before all digit-logs;
  - letter-logs are sorted by content, ties broken by identifier;
  - digit-logs keep their original relative order.
Example: ["dig1 8 1 5 1", "let1 art can", "dig2 3 6", "let2 own kit dig", "let3 art zero"]
      -> ["let1 art can", "let3 art zero", "let2 own kit dig", "dig1 8 1 5 1", "dig2 3 6"]
Hint: sort with a key tuple; Python's sort is stable, so digit-logs can share one key.

Run: python3 reorder_log_files.py
"""


def reorder_logs(logs):
    def key(log):
        ident, content = log.split(" ", 1)
        if content.split(" ", 1)[0].isdigit():
            return (1,)  # digit-logs share one key; stable sort keeps their order
        return (0, content, ident)
    return sorted(logs, key=key)


def _run_tests():
    logs = ["dig1 8 1 5 1", "let1 art can", "dig2 3 6", "let2 own kit dig", "let3 art zero"]
    assert reorder_logs(logs) == [
        "let1 art can", "let3 art zero", "let2 own kit dig", "dig1 8 1 5 1", "dig2 3 6",
    ]
    assert reorder_logs(["let2 a b", "let1 a b"]) == ["let1 a b", "let2 a b"]
    assert reorder_logs(["a1 9 2 3 1", "g1 act car", "zo4 4 7", "ab1 off key dog", "a8 act zoo"]) == [
        "g1 act car", "a8 act zoo", "ab1 off key dog", "a1 9 2 3 1", "zo4 4 7",
    ]
    assert reorder_logs([]) == []
    assert reorder_logs(["d2 1", "d1 2"]) == ["d2 1", "d1 2"]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
