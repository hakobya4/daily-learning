# Day 62, Task 8 -- Git: loose objects vs. packfiles, delta chains, `verify-pack`, `count-objects`, and `repack`

## THE TASK

In a SCRATCH repo (`/tmp/day62-lab`, `git init -b main`), find out how Git actually stores objects on disk and when it compresses them as deltas. Never run any of this against a real repository you care about (and never `git gc --prune=now` there). Keep all config repo-local or one-off with `git -c ...`. Answer the questions by actually running the commands.

1. Make 3 commits that each change ONE line of a ~2000-line text file (e.g. `seq 1 2000 > big.txt`, then edit a line, commit, repeat). Look inside `.git/objects/` with `find .git/objects -type f`: how many loose objects are there and which kinds (`git cat-file -t`)? How big is each blob version on disk (`ls -l` of the object file) compared with the raw file size, and why is every version stored IN FULL even though only one line changed? What compression is applied to a loose object (try `python3 -c "import zlib,sys; print(zlib.decompress(open(sys.argv[1],'rb').read())[:30])" .git/objects/xx/yyyy...`) and what is the header you see before the content?
2. Run `git count-objects -v` before and after `git gc` (or `git repack -a -d`). Explain every line of its output (`count`, `size`, `in-pack`, `packs`, `size-pack`, `prune-packable`, `garbage`, `size-garbage`). What files appeared in `.git/objects/pack/` (`.pack`, `.idx`, maybe `.rev`/`.bitmap`) and what is each for?
3. Run `git verify-pack -v .git/objects/pack/pack-*.idx`. For each blob version of `big.txt`, read the columns (SHA, type, size, size-in-packfile, offset, depth, base SHA). Which version is stored whole and which as a delta -- and is the full one the OLDEST or the NEWEST version? Why does Git prefer that direction? What does the "chain length = N: M objects" histogram at the bottom tell you?
4. Experiment with `git repack -a -d -f --depth=1 --window=1` vs. `--depth=50 --window=250` on a repo with ~20 versions of the file (script it in a loop). Compare `size-pack` and the max chain depth. What do `--window` and `--depth` trade off (pack size vs. CPU at repack time vs. CPU when reading a deep object)? What does `-f` change? Finally: what do `git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(objectsize:disk) %(deltabase)' --batch-all-objects` and `git rev-list --objects --all --disk-usage` add, and how would you use them to find the files that bloat a real repository?

## WHAT I RAN

```bash
# TODO: paste the commands you actually ran, grouped by question
```

## WHAT I OBSERVED

1. **Loose objects, full copies, zlib header:** TODO
2. **`count-objects -v` before/after, files in `objects/pack/`:** TODO
3. **`verify-pack -v` columns, delta direction, chain histogram:** TODO
4. **`--window` / `--depth` / `-f` trade-offs, finding bloat:** TODO

## WHAT SURPRISED ME

- TODO

## ONE-LINE TAKEAWAY

TODO
