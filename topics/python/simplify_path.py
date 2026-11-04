"""
Day 44, Task 3 -- Python: simplify a Unix path.

THE PROBLEM
------------
simplify_path(path) returns the canonical form of an absolute Unix path:
starts with a single "/", no trailing "/", repeated slashes collapsed, "."
removed, ".." pops the previous directory (at the root it does nothing).
Names like "..." are ordinary directory names.
Hint: split on "/" and keep a stack.

Run: python3 simplify_path.py
"""


def simplify_path(path):
    stack = []
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return "/" + "/".join(stack)


def _run_tests():
    assert simplify_path("/home/") == "/home"
    assert simplify_path("/../") == "/"
    assert simplify_path("/home//foo/") == "/home/foo"
    assert simplify_path("/a/./b/../../c/") == "/c"
    assert simplify_path("/a/../../b/../c//.//") == "/c"
    assert simplify_path("/...") == "/..."
    assert simplify_path("/") == "/"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
