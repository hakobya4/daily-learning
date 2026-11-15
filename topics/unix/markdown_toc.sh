#!/usr/bin/env bash
#
# Day 56, Task 6 -- Unix/shell: generate a Markdown table of contents with GitHub-style anchors.
#
# THE PROBLEM
# ------------
# Usage: ./markdown_toc.sh FILE
# A HEADING is a line that starts (column 1) with 1-6 '#' characters followed by ONE space
# and the title text. Not headings:
#   * "#NoSpace" (no space after the hashes), "    ## indented" (not in column 1),
#   * anything inside a fenced code block: a line starting with ``` opens a fence and the
#     next line starting with ``` closes it (the fence lines themselves are not headings).
# A closing run of hashes is stripped: "## API Reference ##" has title "API Reference".
# Trim surrounding whitespace from titles.
#
# For every heading, in order, print
#     <indent>- [<title>](#<slug>)
# where <indent> is two spaces per level BELOW the shallowest heading level in the file
# (if the shallowest is "#", a "###" heading gets 4 spaces), and <slug> is:
#   lowercase the title, delete every character that is not [a-z0-9], space or '-',
#   then replace each space with '-' (do NOT squeeze: "Linux & macOS" -> "linux--macos").
#   The first time a slug appears it is used as-is; the k-th repeat gets "-k" appended
#   ("getting-started", then "getting-started-1", "getting-started-2", ...).
# If the file ends while a fence is still open, print NOTHING on stdout, print
# "unclosed code fence" on stderr and exit 2. A file with no headings prints nothing, exit 0.
# Exit 1 with a usage message on stderr if the argument count is wrong or FILE is not a
# readable regular file.
#
# HINT: a single awk program is enough: a `fence` toggle on /^```/, `match($0, /^#+ /)`
# for the level (reject levels > 6), gsub() to strip the trailing hashes and trim, and
# tolower() + gsub(/[^a-z0-9 -]/, "") + gsub(/ /, "-") for the slug. Keep an associative
# array of slug counts. Because the indent depends on the MINIMUM level over the whole
# file (and the fence error must suppress all output), buffer the headings and print
# them in END.
#
# Check with:
#   cat > /tmp/d56.md <<'MD'
#   # Project Title
#   Intro text.
#   ## Getting Started
#   ### Install (Linux & macOS)
#   ```bash
#   # not a heading
#   ## also not a heading
#   ```
#   ### Install (Linux & macOS)
#   ## API Reference ##
#   #NoSpace is not a heading
#   #### Deep Level
#   ## Getting Started
#       ## indented four spaces is code, not a heading
#   ## FAQ: What's new in v2.0?
#   MD
#   ./markdown_toc.sh /tmp/d56.md
#   (remove the leading "#   " from each line above when you create the file)
# Expected stdout:
#   - [Project Title](#project-title)
#     - [Getting Started](#getting-started)
#       - [Install (Linux & macOS)](#install-linux--macos)
#       - [Install (Linux & macOS)](#install-linux--macos-1)
#     - [API Reference](#api-reference)
#         - [Deep Level](#deep-level)
#     - [Getting Started](#getting-started-1)
#     - [FAQ: What's new in v2.0?](#faq-whats-new-in-v20)
# Then append a line "```" with no closing fence:  printf '```\nx\n' >> /tmp/d56.md
# and the script must print only "unclosed code fence" on stderr and exit 2.

if [ "$#" -ne 1 ] || [ ! -f "$1" ] || [ ! -r "$1" ]; then
    echo "usage: $0 FILE" >&2
    exit 1
fi

# TODO: replace this line
echo "not implemented" >&2
exit 1
