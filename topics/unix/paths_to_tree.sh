#!/usr/bin/env bash
#
# Day 57, Task 5 -- Unix/shell: draw a `tree`-style picture from a list of paths.
#
# THE PROBLEM
# ------------
# Usage: ./paths_to_tree.sh FILE
# Each line of FILE is a relative path such as "src/utils/io.py". Build the directory
# tree they imply and print it like the `tree` command (without calling `tree`):
#   * First line is ".".
#   * Every intermediate component is a DIRECTORY; the last component is a FILE unless
#     the line ends with "/" (then it is an explicit, possibly empty, directory) or the
#     same path is also a prefix of another line (then it is a directory).
#   * Normalise: strip a trailing "\r", leading "./" (repeatedly), collapse "//" into
#     "/", ignore blank lines and duplicates.
#   * Children of a directory are sorted by name in byte order (LC_ALL=C), files and
#     directories mixed. Directories are printed with a trailing "/".
#   * Connectors: "├── " for a child that has later siblings, "└── " for the last one;
#     below a non-last child indent with "│   ", below a last child with "    ".
#   * Finish with "D directories, F files".
# Exit 1 with a usage message on stderr if the argument count is wrong or FILE is not a
# readable regular file.
#
# HINT: one awk pass can record, for every prefix, its parent and whether it is a
# directory (keep an "already seen" set so each child is added to its parent once);
# then a recursive awk function walk(path, prefix) prints the children. awk has no
# sort() in POSIX, so sort a small array by hand (insertion sort) -- awk string
# comparison follows the locale, so run it under LC_ALL=C. Remember that awk function
# locals are declared as extra parameters, or the recursion will clobber them.
#
# Check with:
#   printf '%s\n' 'src/main.py' './src/utils/io.py' 'src/utils/__init__.py' 'README.md' \
#     'docs/' '' 'src/main.py' 'tests//test_io.py' 'Makefile' 'src/utils/io.py' \
#     'build/out/' > /tmp/d57.paths
#   ./paths_to_tree.sh /tmp/d57.paths
# Expected stdout:
#   .
#   ├── Makefile
#   ├── README.md
#   ├── build/
#   │   └── out/
#   ├── docs/
#   ├── src/
#   │   ├── main.py
#   │   └── utils/
#   │       ├── __init__.py
#   │       └── io.py
#   └── tests/
#       └── test_io.py
#   6 directories, 6 files

if [ "$#" -ne 1 ] || [ ! -f "$1" ] || [ ! -r "$1" ]; then
    echo "usage: $0 FILE" >&2
    exit 1
fi

# TODO: replace this line
echo "not implemented" >&2
exit 1
