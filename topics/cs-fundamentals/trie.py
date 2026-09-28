"""
Day 7, Task 8 -- CS fundamentals: Trie (prefix tree) from scratch.

THE PROBLEM
------------
Implement a Trie (prefix tree) with:

  insert(word: str) -> None
      Add a word to the trie.
  search(word: str) -> bool
      True only if `word` was inserted EXACTLY (not just as a prefix
      of some longer inserted word).
  starts_with(prefix: str) -> bool
      True if ANY inserted word starts with `prefix` (the prefix
      itself doesn't need to have been inserted as a whole word).

A trie's nodes each hold a mapping of character -> child node, plus a
flag marking "a word ends exactly here". The root node represents the
empty string and holds no character of its own -- it's just the entry
point into the first level of children.

HOW TO WORK THROUGH THIS
-------------------------
Build a TrieNode class first: a dict `children` (char -> TrieNode) and
a bool `is_end`, defaulting to False.

insert: start at the root; for each character in the word, if that
character isn't already a key in the current node's `children`,
create a new TrieNode there; then move down into that child. After
the loop, mark the FINAL node's `is_end = True`.

search: walk the same way, but if at any point the next character
isn't in the current node's `children`, the word was never inserted
-- return False immediately. If you make it through every character,
return the final node's `is_end` (not just True -- "cat" inserted
doesn't mean "ca" was ever inserted as its own word).

starts_with: identical walk to search, but once you've walked every
character in the prefix successfully, return True regardless of
`is_end` -- you just need SOME word to continue from here, not for the
prefix itself to be a complete word.

Run: python3 trie.py
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


def _run_tests() -> None:
    t = Trie()
    for word in ["cat", "car", "card", "dog"]:
        t.insert(word)

    assert t.search("cat") is True
    assert t.search("car") is True
    assert t.search("card") is True
    assert t.search("dog") is True

    assert t.search("ca") is False       # never inserted as its own word
    assert t.search("cards") is False    # not inserted at all
    assert t.search("do") is False

    assert t.starts_with("ca") is True    # "cat" and "car" both start with "ca"
    assert t.starts_with("car") is True
    assert t.starts_with("do") is True
    assert t.starts_with("dogs") is False  # no inserted word starts with "dogs"
    assert t.starts_with("z") is False

    empty = Trie()
    assert empty.search("anything") is False
    assert empty.starts_with("a") is False

    print("All trie tests passed.")


if __name__ == "__main__":
    _run_tests()
